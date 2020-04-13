#!/usr/bin/env python
import json
import os
import sys

sys.path.append("waveglow")
import threading
import io
import torch
import time
import numpy as np
from collections import OrderedDict

from flask import Flask, flash, request, redirect, url_for, send_file
import numpy as np

import librosa
import librosa.display

import torch

from scipy.io import wavfile
from pydub import AudioSegment

from hparams import create_hparams
from model import Tacotron2
from layers import TacotronSTFT, STFT
from audio_processing import griffin_lim
from train import load_model
from text import text_to_sequence
from denoiser import Denoiser

import audio

semaphore = threading.Semaphore()

hparams = create_hparams()
hparams.sampling_rate = 22050

checkpoint_path = "tacotron2_statedict.pt"
model = load_model(hparams)
model.load_state_dict(torch.load(checkpoint_path)["state_dict"])
_ = model.cuda().eval().half()

waveglow_path = "waveglow_256channels.pt"
waveglow = torch.load(waveglow_path)["model"]
waveglow.cuda().eval().half()
for k in waveglow.convinv:
    k.float()
denoiser = Denoiser(waveglow)


def infer(text):

    # NOTE: Outdated pytorch usage?

    sequence = np.array(text_to_sequence(text, ["english_cleaners"]))[None, :]
    sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

    with torch.no_grad():
        mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
        audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)
        # NOTE: Do we want the denoiser?
        audio_denoised = denoiser(audio, strength=0.01)[:, 0]
        return audio_denoised.cpu().numpy()


def np_to_wav(arr):
    arr = arr[0] * (32767 / max(0.01, np.max(np.abs(arr))))
    as_int16 = arr.astype(np.int16)
    out = io.BytesIO()
    wavfile.write(out, hparams.sampling_rate, as_int16)
    return out


app = Flask(__name__)


@app.route("/", methods=["POST"])
def generate():

    args = request.json
    text = args["text"]
    print(f"Text: {text}")

    try:
        with semaphore:
            waveform = infer(text)

    except Exception as exc:
        print(f"Exception with text: {text}")
        print(exc)
        return "Bad Request", 400

    wav = np_to_wav(waveform)
    
    seg = AudioSegment(wav)
    seg = audio.de_esser(seg)
    wav = io.BytesIO()
    seg.export(wav, format="wav")
    wav.seek(0)

    return send_file(wav, mimetype="audio/wav")


def main():
    app.run(host="0.0.0.0", debug=True, port=6000)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
import json
import os

from flask import Flask, flash, request, redirect, url_for, jsonify
import tensorflow as tf
import numpy as np


import model, sample, encoder
from text import extract_sentences

global graph
graph = tf.get_default_graph()

batch_size = 1
seed = 123
model_name = "run2"
temperature = 1
top_k = 40
nsamples = 1
length = 150
# graph = None


enc = encoder.get_encoder(model_name)
hparams = model.default_hparams()
with open(os.path.join("models", model_name, "hparams.json")) as f:
    hparams.override_from_dict(json.load(f))

# length = hparams.n_ctx


gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)

sess = tf.Session(graph=graph, config=tf.ConfigProto(gpu_options=gpu_options))

np.random.seed(seed)

context = tf.placeholder(tf.int32, [batch_size, None])

output = sample.sample_sequence(
    hparams=hparams,
    length=length,
    # start_token=enc.encoder["<|endoftext|>"],
    context=context,
    batch_size=batch_size,
    temperature=temperature,
    top_k=top_k,
)[:, 1:]

saver = tf.train.Saver()
ckpt = tf.train.latest_checkpoint(os.path.join("models", model_name))
saver.restore(sess, ckpt)
# out = sess.run(output)

app = Flask(__name__)


@app.route("/", methods=["POST"])
def generate():

    args = request.json

    raw_text = args["seed"]
    print(f"Input: {raw_text}")
    context_tokens = enc.encode(raw_text)

    out = sess.run(
        output, feed_dict={context: [context_tokens for _ in range(batch_size)]}
    )[:, len(context_tokens) :]
    text = enc.decode(out[0])
    return jsonify(text=extract_sentences(text))


def main():
    app.run(host="0.0.0.0", debug=True, port=5000)


if __name__ == "__main__":
    main()

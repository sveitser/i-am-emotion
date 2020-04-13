#!/usr/bin/env python
import json
import os
import tempfile
import sys
import time
from contextlib import contextmanager
from io import BytesIO
import multiprocessing as mp

import anyio
import asks
import pyaudio
import trio
import trio_click as click
import wave
from collections import namedtuple, deque

from camera import capture_picture
from range_sensor import get_distance
from led import solid, breathe

MockResponse = namedtuple("MockResponse", ["status_code", "content"])


chunk = 1024
HOST = "localhost"
ACTIVE_DISTANCE_THRESHOLD_CM = 40
CHAIR_COLOR = [0, 0, 1]
MAX_QUEUE_SIZE = 5
audio_queue = mp.Queue()
audio_queue_size = mp.Value("i", 0)
MOCK_BACKEND = False
CONTEXT_TEMPLATE = "I am {emotion}. Can you help me?"
BETWEEN_SENTENCE_SECONDS = 1
NUMBER_LOW_READINGS = 5


@contextmanager
def tempinput(data):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(data)
    temp.close()
    try:
        yield temp.name
    finally:
        os.unlink(temp.name)


async def get_seed(img):
    print("Fetching emotion with image...")
    # Neet a filename, cannot use BytesIO

    if MOCK_BACKEND:
        await trio.sleep(1)
        return "This is the fake seed."

    try:
        with tempinput(img.read()) as tmpfilename:
            resp = await asks.post(f"http://{HOST}:4000", files={"image": tmpfilename})
        emotion, gender = resp.json()
    except Exception as exc:
        print("Exception fetching emotions:", exc)
        emotion, gender = "happy", "woman"

    print(f"got labels: {emotion} {gender}")
    seed = CONTEXT_TEMPLATE.format(emotion=emotion, gender=gender)
    print(f"using seed: {seed}")
    return seed


async def get_text(seed):
    print(f"Fetching text with seed: {seed}")
    if MOCK_BACKEND:
        return ["GENERATED TEXT", "MORE TEXT"]
    resp = await asks.post(f"http://{HOST}:5000", json={"seed": seed})
    text = resp.json()["text"]
    print(f"Received sentences: {' '.join(text)}")
    return text


async def get_audio(text):
    # text = "Hello. How are you?"
    print(f"Fetching audio: {text}")
    if MOCK_BACKEND:
        resp = MockResponse(200, "AUDIO")
    else:
        resp = await asks.post(f"http://{HOST}:6000", json={"text": text})
    return resp


async def fetcher(send_channel, seed):
    sentences = [seed]
    while True:

        try:
            sentences = await get_text(" ".join(sentences))
        except Exception as exc:
            print("Exception getting text: ", exc)
            await trio.sleep(1)
            continue

        for sentence in sentences:

            while audio_queue_size.value >= MAX_QUEUE_SIZE:
                print("waiting...")
                await trio.sleep(1)

            try:
                resp = await get_audio(sentence)
            except Exception as exc:
                print(f"Exception with text: {sentence}")
                await trio.sleep(1)

            else:
                if resp.status_code == 200:

                    audio_queue.put(resp.content)

                    with audio_queue_size.get_lock():
                        audio_queue_size.value += 1
                else:
                    print(f"No audio: status {resp.status_code}")


def cue_from_file(fname):

    with open(fname, "rb") as f:
        message = f.read()

    print(f"Scheduling {fname}")
    audio_queue.put(message)


def player():

    p = pyaudio.PyAudio()

    while True:

        audio_snippet = audio_queue.get()

        with audio_queue_size.get_lock():
            audio_queue_size.value -= 1

        play(p, audio_snippet)

        time.sleep(BETWEEN_SENTENCE_SECONDS)

    # close PyAudio
    p.terminate()


def play(p, audio_snippet):

    if MOCK_BACKEND:
        print("FAKE PLAYING ...")
        time.sleep(3)
        return

    f = wave.open(BytesIO(audio_snippet), "rb")

    def callback(in_data, frame_count, time_info, status):
        data = f.readframes(frame_count)
        return data, pyaudio.paContinue

    stream = p.open(
        format=p.get_format_from_width(f.getsampwidth()),
        channels=f.getnchannels(),
        rate=f.getframerate(),
        output=True,
        stream_callback=callback,
    )
    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()


async def loop_audio(seed):
    async with trio.open_nursery() as nursery:
        send_channel, receive_channel = trio.open_memory_channel(5)
        nursery.start_soon(fetcher, send_channel, seed)
        # nursery.start_soon(player, receive_channel)


def state_transition(current_state, distance):
    if current_state == "idle" and distance <= ACTIVE_DISTANCE_THRESHOLD_CM:
        return "start", "active"
    elif current_state == "active" and distance > ACTIVE_DISTANCE_THRESHOLD_CM:
        return "stop", "idle"
    else:
        return "noop", current_state


def idle():
    solid(*CHAIR_COLOR)


async def seed_prediction(send_channel):
    async with trio.open_nursery() as nursery:
        # white to get a better picture
        # nursery.start_soon(run_sync(), solid, 1, 1, 1)
        solid(1, 1, 1)
        print("taking picture ...")
        img = await trio.run_sync_in_worker_thread(capture_picture)
        print("took picture")
        await trio.sleep(2)
        cue_from_file("photo.wav")
        await trio.sleep(3)

        seed = await get_seed(img)
        print("got seed: ", seed)
        await send_channel.send(seed)


def play_welcome_message():
    cue_from_file("welcome.wav")


async def start_session():

    send_channel, receive_channel = trio.open_memory_channel(0)

    async with trio.open_nursery() as nursery:

        nursery.start_soon(seed_prediction, send_channel)
        play_welcome_message()

        seed = await receive_channel.receive()
        nursery.start_soon(loop_audio, seed)
        nursery.start_soon(breathe, *CHAIR_COLOR)


async def monitor_occupancy(send_channel):

    state = "idle"
    distances = deque(maxlen=NUMBER_LOW_READINGS)
    while True:

        distance = await trio.run_sync_in_worker_thread(get_distance)

        # BS reading
        if distance > 60:
            print(f"Bad reading of Distance: {distance} cm ignoring")
            continue

        distances.append(distance)
        min_dist = min(distances)
        transition, state = state_transition(state, min_dist)
        print(
            f"occupancy: d {distance} min_d {min_dist} state {state} transition {transition}"
        )

        await send_channel.send(transition)


async def run(player_process):

    with trio.CancelScope() as cancel_scope:
        async with trio.open_nursery() as nursery:

            send_channel, receive_channel = trio.open_memory_channel(0)

            idle()
            nursery.start_soon(monitor_occupancy, send_channel)

            while True:
                transition = await receive_channel.receive()
                # print(f"received transition: {transition}")

                if transition == "start":

                    print("starting ...")
                    nursery.start_soon(start_session)

                elif transition == "stop":

                    print("stopping ...")
                    cancel_scope.cancel()
                    terminate(player_process)
                    break


def terminate(proc):
    idle()
    proc.terminate()
    proc.join()
    audio_queue.close()
    print("TERMINATED")


def exit(code=0):
    sys.exit(code)


@click.command()
@click.option("--seed", "-s", default=" ", help="Text seed.")
@click.option("--host", "-h", default="localhost")
@click.option("--color", "-c", default="0 0 1")
@click.option("--context-template", default=CONTEXT_TEMPLATE)
@click.option("--mock_backend", default=False, is_flag=True)
async def main(seed, host, color, mock_backend, context_template):

    global HOST, CHAIR_COLOR, MOCK_BACKEND, CONTEXT_TEMPLATE

    HOST = host
    CHAIR_COLOR = [float(i) for i in color.split()]
    MOCK_BACKEND = mock_backend
    CONTEXT_TEMPLATE = context_template

    print("HOST", HOST)
    print("COLOR", CHAIR_COLOR)
    print("MOCK_BACKEND", MOCK_BACKEND)
    print("CONTEXT_TEMPLATE", CONTEXT_TEMPLATE)

    player_process = mp.Process(target=player)
    player_process.start()

    try:
        await run(player_process)
    except KeyboardInterrupt:
        print("Caught exception ...")

    except Exception as exc:
        print(exc)
        raise
    finally:
        print("finished this run ...")
        terminate(player_process)
        time.sleep(1)

        try:
            import RPi.GPIO as GPIO

            print("Cleaning up GPIO ...")
            GPIO.cleanup()
        except ImportError:
            print("Nothing to clean up....")

    exit(0)


if __name__ == "__main__":
    main(_anyio_backend="trio", auto_envvar_prefix="CHAIR")

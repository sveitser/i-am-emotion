#!/usr/bin/env python
import time
import warnings
from io import BytesIO


class MockCamera:
    def capture(self, stream, **_):
        time.sleep(2)
        with open("../emo/images/test_image.jpg", "rb") as f:
            b = f.read()
        stream.write(b)


try:
    from picamera import PiCamera

    camera = PiCamera()
except Exception as exc:
    print(exc)
    warnings.warn("\nCould NOT import PiCamera. Using Mock.\n")
    camera = MockCamera()


def capture_picture():
    stream = BytesIO()
    print("capturing ...")
    camera.capture(stream, format="jpeg")
    print("done capturing")
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    # image = Image.open(stream)
    return stream

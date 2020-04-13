#!/usr/bin/env python
import warnings


class PWM:
    def start(self, *args):
        pass

    def ChangeDutyCycle(self, *args):
        pass


class MockGPIO:
    def setup(self, *args):
        print(f"GPIO setup {args}")

    def input(self, *args):
        print(f"GPIO input {args}")

    def output(self, *args):
        print(f"GPIO output {args}")

    def setmode(self, *args):
        print(f"GPIO setmode {args}")

    @property
    def BOARD(self,):
        return "BOARD"

    @property
    def IN(self):
        return "IN"

    @property
    def OUT(self):
        return "OUT"

    @property
    def OUT(self):
        return "OUT"

    def PWM(self, *args):
        return PWM()


try:
    import RPi.GPIO as GPIO
except ImportError as exc:
    print(exc)
    warnings.warn("Could not import GPIO. Using Mock.")
    GPIO = MockGPIO()

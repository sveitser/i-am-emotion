import trio
from gpio import GPIO

GPIO.setmode(GPIO.BOARD)
# 15 RED
# 16 GREEN
# 36 BLUE
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)

p1 = GPIO.PWM(15, 500)  # channel=12 frequency=50Hz
p2 = GPIO.PWM(16, 500)  # channel=12 frequency=50Hz
p3 = GPIO.PWM(36, 500)  # channel=12 frequency=50Hz


async def breathe(r, g, b):

    p1.start(0)
    p2.start(0)
    p3.start(0)

    print("starting breathing ...")
    while True:
        for dc in range(0, 101, 2):
            p1.ChangeDutyCycle(dc * r)
            p2.ChangeDutyCycle(dc * g)
            p3.ChangeDutyCycle(dc * b)
            await trio.sleep(0.04)

        for dc in range(100, -1, -2):

            p1.ChangeDutyCycle(dc * r)
            p2.ChangeDutyCycle(dc * g)
            p3.ChangeDutyCycle(dc * b)
            await trio.sleep(0.04)


def solid(r, g, b):

    print("setting solid light: ", r, g, b)

    p1.start(0)
    p2.start(0)
    p3.start(0)

    p1.ChangeDutyCycle(100 * r)
    p2.ChangeDutyCycle(100 * g)
    p3.ChangeDutyCycle(100 * b)

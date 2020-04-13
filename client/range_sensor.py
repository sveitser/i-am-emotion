import time
from gpio import MockGPIO, GPIO

GPIO.setmode(GPIO.BOARD)

# TRIG = 21
# ECHO = 20
TRIG = 40
ECHO = 38


def get_distance():
    # print("Distance Measurement In Progress")

    if isinstance(GPIO, MockGPIO):
        time.sleep(2)
        return 15

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    # print("Waiting For Sensor To Settle")
    time.sleep(1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print("Distance:", distance, "cm")

    return distance

    # GPIO.cleanup()

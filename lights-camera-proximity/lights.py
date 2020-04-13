import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
#15 RED
#16 GREEN
#36 BLUE
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)

p1 = GPIO.PWM(15, 500)  # channel=12 frequency=50Hz
p2 = GPIO.PWM(16, 500)  # channel=12 frequency=50Hz
p3 = GPIO.PWM(36, 500)  # channel=12 frequency=50Hz

p1.start(0)
p2.start(0)
p3.start(0)

try:
    while 1:
        for dc in range(0, 101, 5):
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
            p3.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
            p3.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()

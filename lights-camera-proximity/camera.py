from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.capture('/home/pi/image-new.jpg')

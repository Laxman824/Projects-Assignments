from picamera2 import Picamera2, Preview
import time
from scipy.spatial import distance

import dlib
import cv2
import RPi.GPIO as GPIO

# buzzer setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
BUZZER = 40
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.output(BUZZER, GPIO.LOW)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

----code is private and cannot be viewed----for until further advancement-------------------

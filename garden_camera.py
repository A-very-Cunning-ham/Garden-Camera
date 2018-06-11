from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

import picamera
import numpy as np

from signal import pause
from time import sleep

from subprocess import check_output

lastValue = 0

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')
from subprocess import check_output


GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('GPIOControlIntent', mapping={'status': 'status', 'pin': 'pin'})
def gpio_control(status, pin):

    try:
        pinNum = int(pin)
    except Exception as e:
        return statement('Pin number not valid.')

    GPIO.setup(pinNum, GPIO.OUT)

    if status in ['on', 'high']:    GPIO.output(pinNum, GPIO.HIGH)
    if status in ['off', 'low']:    GPIO.output(pinNum, GPIO.LOW)

    return statement('Turning pin {} {}'.format(pin, status))


@ask.intent('PlantHealth')
def plantHealth():
    healthValue = check_output("python3 cameraSum.py", shell=True)

    if(float(healthValue) > float(lastValue)):
        delta = "up"
    else:
        delta = "down"
    

    diff = str(abs(float(healthValue)-float(lastValue)))

    return statement('Plant health percentage {}%. That is {} {} from last time you checked'.format(healthValue, delta, diff))


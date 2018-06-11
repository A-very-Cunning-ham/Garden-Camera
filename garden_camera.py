# Avery Cunningham
# Smart Garden Camera System
# Adapted from http://www.instructables.com/id/Control-Raspberry-Pi-GPIO-With-Amazon-Echo-and-Pyt/


from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

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

@ask.intent('GPIOControlIntent', mapping={'status': 'status', 'pin': 'pin'}) # Take in pin number and change state on GPIO to match
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
    healthValue = check_output("python3 cameraSum.py", shell=True) # Call the CameraSum.py function and retreive its stdout

    if(float(healthValue) > float(lastValue)): #Determine if health has increased or decreased
        delta = "up"
    else:
        delta = "down"

    diff = str(abs(float(healthValue)-float(lastValue))) #Determine magnitude of change
    
    lastValue = healthValue

    return statement('Plant health percentage {}%. That is {} {} from last time you checked'.format(healthValue, delta, diff))


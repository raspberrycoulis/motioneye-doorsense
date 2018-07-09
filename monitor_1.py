#!/usr/bin/env python
# Import the required modules for Pushover
import requests
import httplib, urllib
import os
from time import sleep

# Import the RPi.GPIO module and warn if not installed:
try:
    import RPi.GPIO as GPIO
except ImportError:
    exit("This script requires the RPi.GPIO module!\nInstall with sudo apt-get install python-rpi.gpio python3-rpi.gpio")

# Some setup first:
APP_TOKEN = 'ADD_YOURS_HERE'    # The app token required for Pushover
USER_TOKEN = 'ADD_YOURS_HERE'   # Ths user token required for Pushover
GPIO.setwarnings(False)         # Stops warnings in the terminal
GPIO.setmode(GPIO.BOARD)        # Set the GPIO mode to use the physical pin number
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

# Functions:
# Get Pushover alerts:
def pushover():
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": APP_TOKEN,                         # Insert app token here
        "user": USER_TOKEN,                         # Insert user token here
        "html": "1",                                # 1 for HTML, 0 to disable
        "title": "Door opened!",                    # Title of the message
        "message": "<b>The door is open!</b>",      # Content of the message
        "url": "http://IP.ADD.RE.SS",               # Link to be included in message
        "url_title": "View on MotionEye OS",        # Text for the link
        "sound": "siren",                           # Define the sound played
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# Update the text overlay on the camera to show as "Open"
def updateTextOpen():
    cameraNumber = "1"
    overlay = "Open"
    requests.post("http://localhost:7999/{camera}/config/set?text_left={text}".format(camera=cameraNumber, text=overlay))

# Update the text overlay on the camera to show as "Closed"
def updateTextClose():
    cameraNumber = "1"
    overlay = "Closed"
    requests.post("http://localhost:7999/{camera}/config/set?text_left={text}".format(camera=cameraNumber, text=overlay))

# Detect if the door is open or closed:
def GPIO_detect():
    if GPIO.input(10):
        print("Closed")
        updateTextClose()   # Update the text on the camera in MotionEye OS
    else:
        print("Open")
        updateTextOpen()    # Update the text on the camera in MotionEye OS
        pushover()          # Call the Pushover function to alert you

try:
    GPIO_detect()
finally:
    GPIO.cleanup()

#!/usr/bin/env python

##############################################################################
# This script will allow you to show the status of a magnetic door switch in #
# MotionEye OS, as well as via push notifications using Pushover.            #
#                                                                            #
# By Wesley Archer (AKA. @raspberrycoulis)                                   #
# https://raspberrycoulis.com | https://github.com/raspberrycoulis           #
##############################################################################

# Import the required modules
import RPi.GPIO as GPIO
import httplib, urllib
import os
import sys
from time import sleep

# Some setup first:
APP_TOKEN = 'ADD_YOURS_HERE'    # The app token - required for Pushover
USER_TOKEN = 'ADD_YOURS_HERE'   # Ths user token - required for Pushover
GPIO.setwarnings(False)         # Stops GPIO warnings in the terminal
GPIO.setmode(GPIO.BOARD)        # Set the GPIO mode to use the physical pin number
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

# Functions:
# Get Pushover alerts when the door is open:
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

# Detect if the door is open or closed:
def GPIO_detect():
    if GPIO.input(10):
        print("Closed")
    else:
        print("Open")
        pushover()                  # Call the Pushover function to alert you
        sys.stderr.write("300")     # Wait 300 seconds (5 mins) before checking again - prevents Pushover spamming

# Where the magic happens
try:
    GPIO_detect()   # Detect if the door is open or closed
finally:
    GPIO.cleanup()  # Cleanup the GPIO on exit

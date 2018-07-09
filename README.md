# motioneye-doorsense

Monitor a magnetic door switch in MotionEye OS and trigger alerts when it is open. Sends Pushover notifications as well as alerts in MotionEye OS.

## Setup

In order to use this script, you will need to be running [MotionEye OS](https://github.com/ccrisan/motioneyeos/wiki) on your Raspberry Pi. The script assumes you have connected your magnetic door switch to GPIO number 10 on the Raspberry Pi and the 3V pin. If you change the GPIO pin, be sure to update the relevant parts in the `monitor_1.py` code accordingly first.

This script assumes you have a [Pushover account](https://pushover.net), and have **paid for full access.** You will then be provided with your **app** and **user tokens**, which are _essential_ for this script to work.

If you want to create a new Pushover app, I have also included an app icon that you can find as `/image/pushover.png`. It is already optimised for Pushover, so feel free to use!

## Install path

MotionEye OS works slightly differently than other Raspberry Pi OS's as the data partition is mounted as read-only by default, but thankfully the location we'll be adding the script is read-write. Whilst `git clone git@github.com:raspberrycoulis/motioneye-doorsense.git` would work great on other Raspberry Pi OS's, on MotionEye OS it is much simpler to create the script manually by copying and pasting the code in `monitor_1.py` accordingly:

```bash
cd /data/etc
nano monitor_1
```

Then paste the contents of `monitor_1.py` into the file, but be sure to update some of the key variables inside:

```python
APP_TOKEN = 'ADD_YOURS_HERE'    # The app token required for Pushover
USER_TOKEN = 'ADD_YOURS_HERE'   # Ths user token required for Pushover
```

And also:

```python
# Update the variables accordingly:
def updateTextOpen():
    cameraNumber = "1"  # Edit accordingly to display the text on the relevant camera. 1 is default.
    overlay = "Open"    # This is the text that will appear on the camera overlay. Open is default.
    requests.post("http://localhost:7999/{camera}/config/set?text_left={text}".format(camera=cameraNumber, text=overlay))

  # Update the variables accordingly:
  def updateTextClose():
      cameraNumber = "1"  # Edit accordingly to display the text on the relevant camera. 1 is default.
      overlay = "Closed"    # This is the text that will appear on the camera overlay. Closed is default.
      requests.post("http://localhost:7999/{camera}/config/set?text_left={text}".format(camera=cameraNumber, text=overlay))
```

Then finally:

```bash
CTRL+X
Y
```

This will exit and save the script. **Be sure to save the file as `monitor_1` without the `.py` extension for it to work!**

## Running

The script should run automatically every second thanks to the built in configuation on MotionEye OS. If you find that you are being bombarded with Pushover notifications, just comment it out in the `GPIO_detect()` function - i.e.:

```python
def GPIO_detect():
    if GPIO.input(10):
        print("Closed")
        updateTextClose()   # Update the text on the camera in MotionEye OS
    else:
        print("Open")
        updateTextOpen()    # Update the text on the camera in MotionEye OS
        #pushover()          # Call the Pushover function to alert you - comment out to stop.
```

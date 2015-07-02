#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import max7219.led as led
from max7219.font import proportional, CP437_FONT

device = led.matrix()

device.show_message("Seconds left:", font=proportional(CP437_FONT))

time.sleep(5)

x=90

while x>0:
    device.show_message(str(x))
    x-= 10
    time.sleep(10)



#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#led = 18

#GPIO.setup(led, GPIO.OUT)

#GPIO.output(led, 1)
#time.sleep(5)
#GPIO.output(led, 0)

#GPIO.cleanup()


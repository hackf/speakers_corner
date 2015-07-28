#!/usr/bin/python

import RPi.GPIO as GPIO


#while x>0:
#    device.show_message(str(x))
#    x-= 10
#    time.sleep(10)



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 17

GPIO.setup(button, GPIO.IN)

while True:
    if (GPIO.input(button)):
        print "Pressed"


#GPIO.output(led, 1)
#time.sleep(5)
#GPIO.output(led, 0)

#GPIO.cleanup()


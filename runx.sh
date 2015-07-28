#!/bin/bash

startx &
sleep 5
export DISPLAY=:0
xset s off; xset -dpms; xset s noblank
xhost +

sleep 2

cd /home/pi/speakers-corner
sudo python speaker.py


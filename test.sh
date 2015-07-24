#!/bin/bash

# For running program during development. Not intended for production use.
export DISPLAY=:0

git pull origin
sudo python speaker.py
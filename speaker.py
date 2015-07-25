__author__ = 'wackyvorlon'

from Tkinter import *
from PIL import ImageTk, Image
import glob
import tkFont
import re
#import picamera
import os
import time
import max7219.led as led  # For LED matrix display
from max7219.font import proportional,CP437_FONT
import subprocess



# TODO Add Raspberry pi camera and GPIO code


# maxwidth = 5  # Sets the maximum number of columns if images in the window

def countdown():
    """
    Implements countdown display on LED matrix, and controls video length.

    :return:
    """
    #Initialize display
    device = led.matrix()

    #Display message at beginning of recording.
    device.show_message("Seconds left:", font=proportional(CP437_FONT))
    time.sleep(1) # Wait for message to display

    x=90 # Maximum length of video.
    while x>0:
        device.show_message(str(x))
        print("Counting...")
        print(x)
        x-=10
        time.sleep(10)


def parsegeom(geometry):
    """
    Parses window geometry
    Code thanks to: http://effbot.org/tkinterbook/wm.htm

    :param geometry:
    :return:
    """
    m = re.match("(\d+)x(\d+)([-+]\d+)[-+]+\d+", geometry)
    # print(m)
    if not m:
        raise ValueError("failed to parse geometry string")
    return map(int, m.groups())





def setup_camera():
    """
    Configure the camera and bind things.
    :return:
    """

    root.after(2000, camerate)

def touch(fname):
    """
    Creates an empty file
    :param fname: Filename to create
    :return:
    """

    with open(fname, 'a'):
        os.utime(fname, None)

def camerate():
    """
    Handles camera things.
    :return:
    """

    print("Camerating...")

    # Start subprocess to record audio and video
    pid = subprocess.Popen(['/home/pi/picam-1.3.0-binary/picam', '--alsadev', 'hw:1,0', '--preview'])
    time.sleep(2)
    # Send start_record command to subprocess
    touch('/home/pi/speakers-corner/hooks/start_record')

    countdown()
    time.sleep(1)
    touch('/home/pi/speakers-corner/hooks/stop_record')
    time.sleep(2)
    pid.kill()


def sponsor_background():
    """
    Set background image from sponsors.
    :return:
    """
    images=[]

    for im in glob.glob('images/*.jpg'):
        images.append(im)

    #change_image(images)
    root.after(5000,change_image,images)


def change_image(im):
    global back
    if not im: # We've exhausted images, start over
        sponsor_background()
        return

    fname=im.pop()
    image = Image.open(fname)
    size = parsegeom(root.geometry())
    sized = size[0], size[1]
    print sized
    image.thumbnail(sized, Image.ANTIALIAS) # Resize to fit screen
    tkimage = ImageTk.PhotoImage(image)
    if back:
        back.pack_forget() # Remove previous label
    back = Label(root, image=tkimage)
    back.image = tkimage
    back.pack(fill=BOTH, expand=YES)
    root.after(10000,change_image,im)


if __name__ == '__main__':

    # Initialize camera variable
    #camera=picamera.PiCamera()

    # Create root window
    root = Tk()
    back=None

    # Make full screen and hide the cursor
    root.attributes("-fullscreen", True)
    root.configure(cursor='none')

    root.after(500,sponsor_background)

    #setup_camera()


    #root.after(30000, root.quit) # Delay before closing, dev use only


    root.mainloop()

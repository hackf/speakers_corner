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


size = 128, 128  # Size of images to display

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


def show_pics():  # Load images and place on canvas.
    i = 1  # Track rightness
    label = []  # Our image labels

    for fname in glob.glob("images/*.jpg"):
        image = Image.open(fname)
        image.thumbnail(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label.append(Label(frame, image=photo, bg="blue"))
        label[i - 1].image = photo
        label[i - 1].grid(row=0, column=i)
        i += 1

    root.after(750, widther, label)  # Using Tkinter means that width numbers are 0 until
                                     # screen is updated. So we wait 750ms.


def widther(label):
    """
    Adds a dummy label to centre images.
    :param label:
    :return:
    """

    # Padding hack
    # Find out how wide the labels are
    q = 0
    for widthulate in label:
        q += widthulate.winfo_width()

    # Grab window dimensions
    windowsize = parsegeom(root.geometry())
    width = windowsize[0]

    # Calculate requisite padding
    padding = (width - q) / 4  # Number found through experimentation. I have no idea why it's 4.
    padding = abs(padding)     # In case too many images are in file, stop padding from going negative
                               # and killing the program.

    dummy = Label(frame, text=" ", bg="blue")
    dummy.grid(row=0, column=0, padx=padding)


def show_instructions():
    """
    Displays the instruction label.

    :return:
    """
    # inst = "Welcome to Speaker's Corner!\nPress button to begin recording!"

    with file("images/inst.txt") as f:
        inst = f.read(100) # Maximum of 100 characters, more tends to fill the screen.

    # Create our own frame.
    frame2 = Frame(root, bg="blue")
    frame2.pack(side=TOP, fill=BOTH, expand=1)
    helv36 = tkFont.Font(family='Helvetica', size=36, weight="bold")
    label = Label(frame2, text=inst, bg="blue", font=helv36, pady=200, fg="red")
    label.pack()


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


if __name__ == '__main__':

    # Initialize camera variable
    #camera=picamera.PiCamera()

    # Create root window
    root = Tk()

    # Make full screen and hide the cursor
    root.attributes("-fullscreen", True)
    root.configure(cursor='none')

    show_instructions()

    frame = Frame(root, bg="blue")
    frame.pack(fill=BOTH, expand=1)

    show_pics()
    #setup_camera()

    root.after(10000, frame.quit) # Delay before closing, dev use only


    root.mainloop()

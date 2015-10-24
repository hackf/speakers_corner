__author__ = 'wackyvorlon'

from Tkinter import *
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
import glob
import re
import os
import time
import max7219.led as led  # For LED matrix display
from max7219.font import proportional, CP437_FONT
import subprocess


def countdown():
    """
    Implements countdown display on LED matrix, and controls video length.

    :return:
    """
    # Initialize display
    device = led.matrix()

    # Display message at beginning of recording.
    device.show_message("Seconds left:", font=proportional(CP437_FONT))
    time.sleep(1)  # Wait for message to display

    x = 90  # Maximum length of video.
    while x > 0:
        device.show_message(str(x))
        print("Counting...")
        print(x)
        x -= 10
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

    # root.after(2000, camerate)
    root.after(100, checkbutt)


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
    pid = subprocess.Popen([
        '/home/pi/picam-1.3.0-binary/picam',
        '--alsadev',
        'hw:1,0',
        '--preview',
        '--volume',
        '2'
    ])

    time.sleep(2)
    # Send start_record command to subprocess
    touch('/home/pi/speakers-corner/hooks/start_record')

    countdown()
    time.sleep(1)
    touch('/home/pi/speakers-corner/hooks/stop_record')
    time.sleep(2)
    pid.kill()


def remux_video_files():

    ts_file_dir = '/home/pi/speakers-corner/rec'
    # ts_file_dir = '/Users/jeffszusz/projects/hackf/speakerscorner/rec'

    (_, _, ts_files) = os.walk(ts_file_dir).next()

    ts_file_name = ts_files[-1]
    ts_file_path = os.path.join(ts_file_dir, ts_file_name)
    output_mpeg2_path = "{}{}".format(ts_file_path.split('.')[0], '.mpg')
    print('output: ' + output_mpeg2_path)

    # pid =
    subprocess.Popen([
        'ffmpeg',
        '-i',
        ts_file_path,
        '-acodec',
        'copy',
        '-vcodec',
        'copy',
        output_mpeg2_path
    ])

    # pid.kill()


def sponsor_background(images, lbl):
    """
    Set background image from sponsors.
    :return:
    """
    if not images:
        for im in glob.glob('images/*.jpg'):
            images.append(im)

    # Schedule image updating.
    root.after(5000, change_image, images, lbl)


def setup_label():
    images = []

    for im in glob.glob('images/*.jpg'):
        images.append(im)

    fname = images.pop()
    image = Image.open(fname)
    size = parsegeom(root.geometry())  # Grab screen size
    sized = size[0], size[1]
    print sized
    image.thumbnail(sized, Image.ANTIALIAS)  # Resize to fit screen
    tkimage = ImageTk.PhotoImage(image)
    back = Label(root, image=tkimage)
    back.image = tkimage
    back.pack(fill=BOTH, expand=YES)
    sponsor_background(images, back)


def checkbutt():
    """
    Check button state.
    :return:
    """
    if (GPIO.input(button)):
        print "Button pressed!"
        camerate()

    root.after(100, checkbutt)


def change_image(im, lbl):
    """
    Changes background image periodically.
    :param im: list of image filenames
    :return:
    """
    # global back
    if not im:  # We've exhausted images, start over
        sponsor_background(im, lbl)
        return

    fname = im.pop()
    image = Image.open(fname)
    size = parsegeom(root.geometry())  # Grab screen size
    sized = size[0], size[1]
    print sized
    image.thumbnail(sized, Image.ANTIALIAS)  # Resize to fit screen
    tkimage = ImageTk.PhotoImage(image)

    lbl.configure(image=tkimage)
    lbl.image = tkimage
    # Make sure we run to swap the image again.
    root.after(10000, change_image, im, lbl)


if __name__ == '__main__':
    # Configure GPIO
    button = 17  # BCM (Broadcom SOC challen) GPIO 17 is pin #11 on board
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(button, GPIO.IN)
    # root.after(100,checkbutt)

    # Create root window
    root = Tk()
    # back = None

    # Make full screen and hide the cursor
    root.attributes("-fullscreen", True)
    root.configure(cursor='none')

    # Start changing the sponsor background image
    root.after(500, setup_label)

    setup_camera()

    # root.after(130000, root.quit)  # Delay before closing, dev use only

    root.mainloop()

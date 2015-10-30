#  authors: wackyvorlon, jeffszusz, rtopliffe

from Tkinter import *
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
import picamera
import glob
import re
import os
import time
import max7219.led as led  # For LED matrix display
from max7219.font import proportional, CP437_FONT
import subprocess


def countdown():
    """
    Display countdown on LED matrix, updatingn in 10 second intervals
    Determines video recording length

    :return:
    """
    # Initialize display
    matrix = led.matrix()

    # Display message at beginning of recording.
    matrix.show_message("Seconds left:", font=proportional(CP437_FONT))
    time.sleep(1)  # Wait for message to display

    time_remaining = 90  # Maximum length of video in seconds.
    while time_remaining > 0:
        matrix.show_message(str(time_remaining))
        time_remaining -= 10
        time.sleep(10)


def parsegeometry(geometry):
    """
    Parses window geometry
    Code thanks to: http://effbot.org/tkinterbook/wm.htm

    :param geometry:
    :return:
    """
    m = re.match("(\d+)x(\d+)([-+]\d+)[-+]+\d+", geometry)
    if not m:
        raise ValueError("failed to parse geometry string")
    return map(int, m.groups())


def touch(fname):
    """
    Creates an empty file
    :param fname: Filename to create
    :return:
    """

    with open(fname, 'a'):
        os.utime(fname, None)


def poll_button():
    if (GPIO.input(button)):
        begin_recording()

    window.after(100, poll_button)


def begin_recording():
    camera = picamera.PiCamera()

    camera.start_preview()

    time.sleep(20000)

    camera.stop_preview()

    # Start subprocess to record audio and video
    #pid = subprocess.Popen([
        #'/home/pi/picam-1.3.0-binary/picam',
        #'--alsadev',
        #'hw:1,0',
        #'--preview',
        #'--volume',
        #'2'
    #])

    #time.sleep(2)

     #use picam's start_record hook
    #touch('/home/pi/speakers-corner/hooks/start_record')

    #countdown()

    #time.sleep(1)

     #use picam's stop_record hook
    #touch('/home/pi/speakers-corner/hooks/stop_record')
    #time.sleep(2)

    #pid.kill()

    #remux_latest_video_file()


def remux_latest_video_file():
    """
    Repackage the latest MPEG-TS (Transport Stream) file
    in an MPEG-PS (Program Stream) container
    """

    ts_file_dir = '/home/pi/speakers-corner/rec'
    #ts_file_dir = '/Users/jeffszusz/projects/hackf/speakerscorner/rec'

    (_, _, ts_files) = os.walk(ts_file_dir).next()

    ts_file_name = ts_files[-1]
    ts_file_path = os.path.join(ts_file_dir, ts_file_name)
    mpeg2_output_path = "{}{}".format(ts_file_path.split('.')[0], '.mpg')

    subprocess.Popen([
        'ffmpeg',
        '-i',
        ts_file_path,
        '-acodec',
        'copy',
        '-vcodec',
        'copy',
        mpeg2_output_path
    ])


def sponsor_images():
    """
    returns a generator, provides the next image in the sponsor slideshow
    """

    while True:
        for fname in glob.glob('images/*.jpg'):
            yield Image.open(fname)


def start_sponsor_slideshow():
    images = sponsor_images()
    cycle_through_images(images, None)


def cycle_through_images(images, label):

    image = images.next()

    size = parsegeometry(window.geometry())  # Grab screen size
    sized = size[0], size[1]

    image.thumbnail(sized, Image.ANTIALIAS)  # Resize to fit screen
    tkimage = ImageTk.PhotoImage(image)

    if not label:
        label = Label(window, image=tkimage)

    label.pack(fill=BOTH, expand=YES)
    label.configure(image=tkimage)
    label.image = tkimage

    window.after(10000, cycle_through_images, images, label)


if __name__ == '__main__':

    button = 17  # BCM (Broadcom SOC challen) GPIO 17 is pin #11 on board
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(button, GPIO.IN)

    window = Tk()

    window.attributes("-fullscreen", True)
    window.configure(cursor='none')

    window.after(500, start_sponsor_slideshow)

    poll_button()

    window.mainloop()

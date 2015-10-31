#  authors: wackyvorlon, jeffszusz, rtopliffe

from Tkinter import Tk, Label, BOTH, YES
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
from max7219 import led  # For LED matrix display
from max7219.font import proportional, CP437_FONT
import picamera
import glob
import os
import time
import subprocess


class SpeakersCorner():

    def __init__(self):

        self.video_length = 90  # seconds
        self.button = 17

        # BCM (Broadcom SOC Channel) GPIO 17 is pin #11 on the board
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.button, GPIO.IN)

        self.window = Tk()
        self.window.attributes("-fullscreen", True)
        self.window.configure(cursor='none')

    def countdown(self):
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

        time_remaining = self.video_length
        while time_remaining > 0:
            matrix.show_message(str(time_remaining))
            time_remaining -= 10
            time.sleep(10)

    def parsegeometry(self, geometry):
        """
        Parses window geometry
        """

        x, y = geometry.split('+')[0].split('x')
        return (x, y)

    def poll_button(self):
        if (GPIO.input(self.button)):
            self.begin_recording()

        self.window.after(100, self.poll_button)

    def begin_recording(self):
        camera = picamera.PiCamera()

        camera.start_preview()

        time.sleep(10000)

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
        #self.touch('/home/pi/speakers-corner/hooks/start_record')

        #self.countdown()

        #time.sleep(1)

         #use picam's stop_record hook
        #self.touch('/home/pi/speakers-corner/hooks/stop_record')
        #time.sleep(2)

        #pid.kill()

        #self.remux_latest_video_file()

    def remux_latest_video_file(self):
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

    def sponsor_images(self):
        """
        returns a generator, provides the next image in the sponsor slideshow
        """

        while True:
            for fname in glob.glob('images/*.jpg'):
                yield Image.open(fname)

    def start_sponsor_slideshow(self):
        images = self.sponsor_images()
        self.cycle_through_images(images, None)

    def cycle_through_images(self, images, label):

        image = images.next()

        size = self.parsegeometry(self.window.geometry())  # Grab screen size
        window_size = size[0], size[1]

        image.thumbnail(window_size, Image.ANTIALIAS)  # Resize to fit screen
        tkimage = ImageTk.PhotoImage(image)

        if not label:
            label = Label(self.window, image=tkimage)

        label.pack(fill=BOTH, expand=YES)
        label.configure(image=tkimage)
        label.image = tkimage

        self.window.after(10000, self.cycle_through_images, images, label)

    def main(self):

        self.window.after(500, self.start_sponsor_slideshow)

        self.poll_button()

        self.window.mainloop()

from __future__ import print_function

import pygame
import glob
import sys
import io
import math
import picamera

# import RPi.RPIO as RPIO
import RPIO

from time import time
from pygame.locals import QUIT
from StringIO import StringIO
from PIL import Image


# Monitor size
WIDTH = 1280
HEIGHT = 720


class SpeakersCorner(object):

    def __init__(self):
        pygame.init()
        print('starting ...')
        self._window = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.FULLSCREEN,
            32
        )
        print('finishing startup ...')
        self._images = self._sponsor_images()
        self._time_displayed = 0.0
        self._button = 17

        # RPIO.setmode(RPIO.BCM)
        RPIO.setwarnings(False)
        RPIO.setup(self._button, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
        self._add_button_callback()

    def _sponsor_images(self):
        """
        returns a generator, provides the next image in the sponsor slideshow
        """

        while True:
            for fname in glob.glob('images/*.jpg'):
                yield Image.open(fname, 'r')

    def _resize_image(self, image):
        width, height = image.size
        print('Image size {} {}'.format(width, height))

        # if the image is smaller then the window size than we don't have to
        # scale it.
        if width < WIDTH and height < HEIGHT:
            return image

        # Find the difference between the two sizes. The largest of the width
        # and height will be used to scale the image down to size
        # Note: We need floats not ints since the ratio will be below 1
        ratio = min(
            float(WIDTH) / float(width),
            float(HEIGHT) / float(height)
        )
        print('ratio: {}'.format(ratio))

        # Apply our ratio to scale the size
        # Image.resize only takes in ints not floats
        size = (
            int(math.floor(width * ratio)),
            int(math.floor(height * ratio))
        )
        print('New Size: {}'.format(size))

        return image.resize(size, resample=Image.ANTIALIAS)

    def _center_dimensions(self, d1, d2):
        return (d1 / 2) - (d2 / 2)

    def _begin_recording(self, *args):
        # TODO - start audio recording
        # http://stackoverflow.com/questions/6867675/audio-recording-in-python
        # https://github.com/waveform80/picamera/issues/191
        print('beginning recording')
        # *args - to catch the additional arguments passed to this function
        # by the callee
        RPIO.stop_waiting_for_interrupts()

        with picamera.PiCamera() as camera:
            camera.resolution = (1280, 720)
            camera.start_preview()
            camera.start_recording('/home/pi/videos/test.h264')
            camera.wait_recording(90)
            camera.stop_recording()
            camera.stop_preview()

        RPIO.wait_for_interrupts(threaded=True)

    def _begin_recording_exp(self, *args):
        """
        WARNING: Experimental function!! Use with caution.

        Instead of using the picamera preview we continuosly take photos and
        display them with pygame.

        http://picamera.readthedocs.org/en/release-1.10/recipes2.html#rapid-capture-and-streaming
        """
        start = time()
        with picamera.PiCamera() as camera:
            stream = io.BytesIO()
            # NOTE: if the program hangs here you gave `capture_continuous` a
            # `format` kwarg it doesn't understand.
            for _ in camera.capture_continuous(stream, format='jpeg',
                                               resize=(800, 600)):
                # Truncate the stream to the current position (in case
                # prior iterations output a longer image)
                stream.truncate()
                stream.seek(0)

                if time() - start > 10:
                    break

                # Need to create a new PIL.Image object so we can pass the byte
                # information to pygame. Pygame had trouble reading directly
                # from the stream and this seems to be the only work around.
                # Need to figure out how to get pygame to directly read from
                # the stream.
                image = Image.open(StringIO(stream.read()))

                try:
                    # convert PIL image into pygame image
                    image = pygame.image.frombuffer(
                        image.tobytes(),
                        image.size,
                        'RGB'
                    )
                except ValueError as error:
                    print(error.message)
                    print('Bad image')
                    continue
                else:
                    self._window.blit(image, (0, 0))
                    pygame.display.flip()

                # resize stream to be zero bytes long
                stream.truncate(0)
                stream.seek(0)

    def _add_button_callback(self):
        print('Setting up interrupt callback')

        RPIO.add_interrupt_callback(
            self._button,
            self._begin_recording,
            edge='rising',
            debounce_timeout_ms=1000
        )

    def clean_up(self):
        RPIO.cleanup()

    def mainloop(self):
        # Runs interrupt callbacks in a thread. Pygame loop will continue to
        # run in the main thread.
        RPIO.wait_for_interrupts(threaded=True)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    self.clean_up()
                    sys.exit(0)

            # only display the next image after 10 seconds
            if time() - self._time_displayed >= 10:
                image = self._images.next()
                image = self._resize_image(image)

                try:
                    # convert PIL image into pygame image
                    image = pygame.image.frombuffer(
                        image.tobytes(),
                        image.size,
                        'RGB'
                    )
                except ValueError:
                    print('Bad image')
                    continue

                # Fill window screen with black. If this isn't done the
                # previous images will appear behind the new ones.
                self._window.fill((0, 0, 0))

                print('Surface size: {} {}'.format(image.get_width(),
                                                   image.get_height()))

                x = self._center_dimensions(WIDTH, image.get_width())
                y = self._center_dimensions(HEIGHT, image.get_height())

                print('Position: {} {}'.format(x, y))
                # display the image at the top left of the screen
                self._window.blit(image, (x, y))

                # reset the time since the last image was displayed
                self._time_displayed = time()

                # update the full display to the screen
                pygame.display.flip()

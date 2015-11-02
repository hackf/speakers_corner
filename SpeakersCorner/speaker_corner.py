from __future__ import print_function

import pygame
import glob
import sys
import math


from time import time
from pygame.locals import QUIT
from PIL import Image


# Monitor size
WIDTH = 1280
HEIGHT = 720


class SpeakersCorner(object):

    def __init__(self):
        pygame.init()
        self._window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        self._images = self._sponsor_images()
        self._time_displayed = 0.0

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

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

            # only display the next image after 10 seconds
            if time() - self._time_displayed >= 10:
                image = self._images.next()
                image = self._resize_image(image)

                # convert PIL image into pygame image
                image = pygame.image.frombuffer(
                    image.tobytes(),
                    image.size,
                    'RGB'
                )

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

from __future__ import print_function
import sys
import signal
from SpeakersCorner import SpeakersCorner


if __name__ == '__main__':
    speakers_corner = SpeakersCorner()

    def handler(*args, **kwargs):
        print(args)
        speakers_corner.clean_up()
        sys.exit(0)

    signal.signal(signal.SIGQUIT, handler)

    try:
        speakers_corner.mainloop()
    except KeyboardInterrupt:
        speakers_corner.clean_up()

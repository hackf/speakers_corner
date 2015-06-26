__author__ = 'wackyvorlon'

from Tkinter import *
from PIL import ImageTk, Image
import glob
import tkFont
import re

size = 128, 128  # Size of images to display

# TODO Add Raspberry pi camera and GPIO code


# maxwidth = 5  # Sets the maximum number of columns if images in the window


def parsegeom(geometry):
    """
    Parses window geometry
    Code thanks to: http://effbot.org/tkinterbook/wm.htm
    :param geometry:
    :return:
    """
    print(geometry)
    m = re.match("(\d+)x(\d+)([-+]\d+)[-+]+\d+", geometry)
    #print(m)
    if not m:
        raise ValueError("failed to parse geometry string")
    return map(int, m.groups())


def show_pics():  # Load images and place on canvas.
    i = 1  # Track rightness


    for file in glob.glob("images/*.jpg"):
        image = Image.open(file)
        image.thumbnail(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label = Label(frame, image=photo, bg="blue")
        # label.image = photo
        # label.pack(side=LEFT)
        label.image = photo
        label.grid(row=1, column=i)
        i += 1

    # Padding hack
    #Find out how wide the window is
    windowsize = parsegeom(root.geometry())
    width=windowsize[0]
    print(width)
    padding=(width- 1000)/2
    print(padding)
    dummy = Label(frame, bg="blue")
    dummy.grid(row=0, padx=padding)


def show_instructions():
    """
    Displays the instruction label.

    :return:
    """
    inst = "Welcome to Speaker's Corner!\nPress button to begin recording!"

    # Create our own frame.
    frame2 = Frame(root, bg="blue")
    frame2.pack(side=TOP, fill=BOTH, expand=1)
    helv36 = tkFont.Font(family='Helvetica', size=36, weight="bold")
    label = Label(frame2, text=inst, bg="blue", font=helv36, pady=200)
    label.pack()


def quitter():
    """
    Add quit button during development.
    :return:
    """
    frame3 = Frame(root, bg="blue")
    frame3.pack(fill=BOTH, expand=1, side=BOTTOM)
    button = Button(frame3, text="QUIT", fg="red", command=frame.quit)
    button.pack(side=BOTTOM)


if __name__ == '__main__':
    root = Tk()
    # root.attributes("-bg", "blue")
    # Fullscreen
    root.attributes("-fullscreen", True)
    show_instructions()

    frame = Frame(root, bg="blue")
    frame.pack(fill=BOTH, expand=1)

    show_pics()

    # TODO Change to false for production
    if True:
        quitter()

root.mainloop()

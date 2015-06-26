__author__ = 'wackyvorlon'

from Tkinter import *
from PIL import ImageTk, Image
import glob
import tkFont

size = 128, 128  # Size of images to display

# TODO Add Raspberry pi camera and GPIO code

# frame = Frame(root, bg="blue")
# frame.grid(row=0)

maxwidth = 5  # Sets the maximum number of columns if images in the window
imagetops = 1  # Initial row the images should appear in
DEV = 0  # Development mode. Change to zero for production.


def show_pics():  # Load images and place on canvas.
    #i = 0  # Track rightness
    #j = imagetops  # Track downness.

    for file in glob.glob("images/*.jpg"):
        image = Image.open(file)
        image.thumbnail(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label = Label(frame, image=photo, bg="blue")
        # label.image = photo
        # label.pack(side=LEFT)
        label.image = photo
        label.pack()




def show_instructions():
    """
    Displays the instruction label.

    :return:
    """
    inst = "Welcome to Speaker's Corner!\nPress button to begin recording!"

    # Create our own frame.
    frame2=Frame(root,bg="blue")
    frame2.pack(side=TOP,fill=BOTH, expand=1)
    helv36 = tkFont.Font(family='Helvetica', size=36, weight="bold")
    label = Label(frame2, text=inst, bg="blue", font=helv36)
    label.pack()


if __name__ == '__main__':
    root=Tk()
    #root.attributes("-bg", "blue")
    # Fullscreen?
    if DEV == 0:
        root.attributes("-fullscreen", True)
    show_instructions()

    frame = Frame(root, bg="blue")
    frame.pack(fill=BOTH,expand=1)

    foo = show_pics()

    # Are we in DEV mode? If so, show quit button.
    if DEV == 0:
        button = Button(frame, text="QUIT", fg="red", bg="blue", command=frame.quit)
        button.pack()



root.mainloop()

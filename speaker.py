__author__ = 'wackyvorlon'

from Tkinter import *
from PIL import ImageTk, Image
import glob

size = 128, 128  # Size of images to display

# TODO Add Raspberry pi camera and GPIO code

root = Tk()

frame = Frame(root, bg="blue")
frame.grid(row=0)

maxwidth = 5    # Sets the maximum number of columns if images in the window
imagetops = 5   # Initial row the images should appear in
DEV=1           #Development mode. Change to zero for production.

def show_pics():  # Load images and place on canvas.
    i = 0  # Track rightness
    j = imagetops  # Track downness.

    for file in glob.glob("images/*.jpg"):
        image = Image.open(file)
        image.thumbnail(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label = Label(frame, image=photo,bg="blue")
        # label.image = photo
        # label.pack(side=LEFT)
        label.image = photo
        label.grid(row=j, column=i)  # Move rightwise
        i += 1
        if i == maxwidth:
            i = 0
            j += 1
    return j

def show_instructions():
    """
    Displays the instruction label.

    :return:
    """
    inst="Welcome to Speaker's Corner! Press button to begin recording!"
    label = Label(frame,text=inst, bg="blue")
    label.grid(row=0,column=0)

if __name__ == '__main__':
    show_instructions()
    show_pics()

# NB: Quit button is only here for development purposes.
if DEV==1:

    button = Button(frame, text="QUIT", fg="red",bg="blue", command=frame.quit)
    button.grid(row=show_pics() + 1, column=maxwidth / 2)  # show_pics()+1 ensures that quit button is below everything.

root.mainloop()

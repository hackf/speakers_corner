__author__ = 'wackyvorlon'

from Tkinter import *
from PIL import ImageTk, Image
import glob

size = 128, 128  # Size of images to display

# TODO Add Raspberry pi camera and GPIO code

root = Tk()

frame = Frame(root)
frame.grid(row=0)



def show_pics():  # Load images and place on canvas.
    i=0 # Track rightness

    for file in glob.glob("images/*.jpg"):
        image = Image.open(file)
        image.thumbnail(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label = Label(image=photo)
        # label.image = photo
        # label.pack(side=LEFT)
        label.image = photo
        label.grid(row=0, column=i)  # Move rightwise
        i = i + 1


show_pics()

button = Button( text="QUIT", fg="red", command=frame.quit)
button.grid(row=1, column=0)

root.mainloop()

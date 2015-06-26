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
    j=0 # Track downness.

    for file in glob.glob("images/*.jpg"):
        image = Image.open(file)
        image.thumbnail(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label = Label(image=photo)
        # label.image = photo
        # label.pack(side=LEFT)
        label.image = photo
        label.grid(row=j, column=i)  # Move rightwise
        i += 1
        if i==3 :
            i=0
            j += 1
    return j


#show_pics()

button = Button( text="QUIT", fg="red", command=frame.quit)
button.grid(row=show_pics()+1, column=0) #show_pics()+1 ensures that quit button is below everything.

root.mainloop()

__author__ = 'wackyvorlon'

from Tkinter import *
from PIL import ImageTk, Image
import glob

size = 128,128  # Size of images to display

root=Tk()

frame=Frame(root)
frame.pack()

for file in glob.glob("*.jpg"):
    image=Image.open(file)
    image.thumbnail(size,Image.ANTIALIAS)
    photo=ImageTk.PhotoImage(image)

    label=Label(image=photo)
    label.image=photo
    label.pack(side=LEFT)

button= Button(frame,text="QUIT", fg="red", command=frame.quit)
button.pack(side=LEFT)

root.mainloop()





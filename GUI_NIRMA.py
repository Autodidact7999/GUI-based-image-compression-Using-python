from tkinter import *
import cv2
import tkinter.filedialog
import numpy as np
from ITC_Support import *
from ITC_main import *
import sys
import PIL.Image
from tkinter import *
import os

root = tkinter.Tk()
root.withdraw()

path =tkinter.filedialog.askopenfilename()
encoded,original = encode(path)

cv2.namedWindow('Compressed Image', cv2.WINDOW_NORMAL)
cv2.imshow('Compressed Image',encoded)

cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
cv2.imshow('Original Image',original)
savefile = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
picture = PIL.Image.open(encoded)
picture.save(savefile)
cv2.waitKey(0)
cv2.destroyAllWindows()
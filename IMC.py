# coding: utf-8

# In[9]:
import os, sys
from tkinter import *
from tkinter import messagebox, Label
import tkinter.filedialog
import tkinter.colorchooser
import math
import cv2
import numpy as np
from ITC_Support import *
from copy import copy
from PIL import Image, ImageTk, ImageFilter, ImageOps


class userInterfaze:

    window_size = "800x600"
    size = 256, 256
    color = "grey"
    filters = {'Image Compresion'}
    acImage = ''
    outImage = ''
    file = 0

    def __init__(self, master):
        global actlmage
        global outImage
        self.master = master
        master.title("NIRMA IMAGE COMPRESSIOR")

        tkvar = StringVar(root)
        tkvar.set('IMAGE COMPRESSION')
        master.geometry(self.window_size)
        master.resizable(width=False, height=False)
        self.window = tkinter.Frame(master)
        self.window.pack()

        inImage = Image.open("intro.jpg")
        actlmage = copy(inImage)
        outImage = copy(inImage)
        inImage.thumbnail(self.size, Image.ANTIALIAS)
        self.tkimage = ImageTk.PhotoImage(inImage)
        self.inMiniaturePanel = tkinter.Label(self.window, image=self.tkimage, width=256, height=256)
        self.inMiniaturePanel.grid(row=0)

        outputimage = Image.open("result.jpg")
        outputimage.thumbnail(self.size, Image.ANTIALIAS)
        self.tkimageout = ImageTk.PhotoImage(outputimage)
        self.outMiniaturePanel = tkinter.Label(self.window, image=self.tkimageout, width=256, height=256)
        self.outMiniaturePanel.grid(row=0, column=2)

        chooseButton = tkinter.Button(self.window, text="SELECT IMAGE", command=self.chooseImage).grid(row=1,
                                                                                                       column=0,
                                                                                                       pady=8)
        saveButton = tkinter.Button(self.window, text="SAVE IMAGE", command=self.saveImage).grid(row=1,
                                                                                                 column=2)
        Label(self.window, text="  ").grid(row=2, column=0)
        filterMenu = OptionMenu(self.window, tkvar, *self.filters).grid(row=2, column=1)  # ComboBox
        filerButton = tkinter.Button(self.window, text="Apply", command=self.aplySteganography).grid(row=2, column=2,
                                                                                                     pady=20)

    def aplySteganography(self):
        global actlmage
        global outImage

        encoded = self.encode(actlmage)

        outImage = copy(encoded)
        self.refreshImages(encoded , self.outMiniaturePanel)


    def chooseImage(self):
        global actlmage
        filename = tkinter.filedialog.askopenfilename()
        if filename:
            try:
                inImage2 = Image.open(filename)  # Abrir Imagen
                actlmage = copy(inImage2)
                self.refreshImages(inImage2, self.inMiniaturePanel)
            except:
                tkinter.messagebox.showerror("Error", "Fail to open File.")

    def refreshImages(self, newMiniatureImage, panel):
        newMiniatureImage.thumbnail(self.size, Image.ANTIALIAS)
        tkimageout = ImageTk.PhotoImage(newMiniatureImage)  # Mostrar imagen
        panel.configure(image=tkimageout)
        panel.image = tkimageout


    def saveImage(self):
        global outImage
        savefile = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if savefile:  # Comprueba si se le dío a cancelar.
            try:
                outImage.save(savefile)
            except:
                messagebox.showerror("Error", "Fallo al abrir el archivo")

    def encode(self, actlamage):
        img = copy(actlmage)

        # resized_image = cv2.resize(img, (256, 256))
        # cv2.imwrite('code_blooded.bmp',resized_image)

        img = np.array(img)
        rows, cols, channel = img.shape
        img_b, img_g, img_r = cv2.split(img)
        o_img_b, o_img_g, o_img_r = cv2.split(img)

        depth = 2

        nodes = pow(2, depth)
        g_encode =self.median_cut(img_g, depth)
        b_encode =self.median_cut(img_b, depth)
        r_encode =self.median_cut(img_r, depth)

        # np.savetxt("green.csv", img_g, delimiter=",")
        # np.savetxt("blue.csv", img_b, delimiter=",")
        # np.savetxt("red.csv", img_r, delimiter=",")

        # lookup table creation
        with open('lookup32.csv', 'w') as file:
            file.write("Green lookup:\n")
            file.write("Start,End,Value\n")
            for i in range(nodes):
                file.write(str(g_encode[i]) + ',' + str(g_encode[i + 1]) + ',' + str(
                    int(g_encode[i] / 2 + g_encode[i + 1] / 2)))
                file.write('\n')
            file.write("Blue lookup:\n")
            file.write("Start,End,Value\n")
            for i in range(nodes):
                file.write(str(b_encode[i]) + ',' + str(b_encode[i + 1]) + ',' + str(
                    int(b_encode[i] / 2 + b_encode[i + 1] / 2)))
                file.write('\n')
            file.write("Red lookup:\n")
            file.write("Start,End,Value\n")
            for i in range(nodes):
                file.write(str(r_encode[i]) + ',' + str(r_encode[i + 1]) + ',' + str(
                    int(r_encode[i] / 2 + r_encode[i + 1] / 2)))
                file.write('\n')

        for i in range(rows):
            for j in range(cols):
                index = self.binarySearch(b_encode, 0, nodes - 1, img_b[i][j])
                if (index != -1):
                    img_b[i][j] = int(b_encode[index] / 2 + b_encode[index + 1] / 2)
                index = self.binarySearch(g_encode, 0, nodes - 1, img_g[i][j])
                if (index != -1):
                    img_g[i][j] = int(g_encode[index] / 2 + g_encode[index + 1] / 2)
                index = self.binarySearch(r_encode, 0, nodes - 1, img_r[i][j])
                if (index != -1):
                    img_r[i][j] = int(r_encode[index] / 2 + r_encode[index + 1] / 2)

        rgb = np.dstack((img_b, img_g, img_r))
        return rgb

    def binarySearch(self,encode, l, h, x):
        " ceil binary search returns index and -1 if not present "
        if l > h:
            return -1
        if x >= (encode[h]):
            return h
        mid = int((l + h) / 2)
        if encode[mid] == x:
            return mid
        if mid > 0 and (encode[mid - 1]) <= x and x < (encode[mid]):
            return mid - 1
        if x < (encode[mid]):
            return binarySearch(encode, l, mid - 1, x)
        return binarySearch(encode, mid + 1, h, x)

    def flatten_image(self , image):

        flat = []
        flat = [x for sublist in image for x in sublist]
        flat = np.array(flat)
        return flat

    def median_cut(self , img, depth):

        img = self.flatten_image(img)
        img.sort()
        n = len(img)
        encode = []
        x = int(n / pow(2, depth))
        for i in range(0, pow(2, depth)):
            encode.append(img[i * x])
        encode.append(img[n - 1])
        return encode

    def SNR(original_img, compressed_img, rows, cols):

        noise = [[0 for x in range(rows)] for y in range(cols)]
        for i in range(rows):
            for j in range(cols):
                if (original_img[i][j] > compressed_img[i][j]):
                    noise[i][j] = original_img[i][j] - compressed_img[i][j]
                else:
                    noise[i][j] = (compressed_img[i][j] - original_img[i][j])
                    noise[i][j] *= -1
        return noise


root = tkinter.Tk()
ui = userInterfaze(root)
root.mainloop()

import tkinter as tk
from Styles import *
from tkinter import filedialog

from PIL import Image, ImageTk

class ImageInputFrame(tk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.configure(borderwidth=2, relief="groove", bg=TAN, bd=0)

        b1 = tk.Button(self, text='Upload File', 
        width=20,command = lambda:self.uploadFile())
        b1.grid(row=0,column=0) 

        self.monsterImage = None
        self.resultImage = tk.Label(self, image='', bg=TAN)
        self.resultImage.grid(row=1, column=0)

    def uploadFile(self):
        f_types = [('Jpg Files', '*.jpg'),
                    ('PNG Files','*.png')]   # type of files to select 
        filename = filedialog.askopenfilename(filetypes=f_types)
        img = Image.open(filename)
        self.monsterImage = ImageTk.PhotoImage(img)
        self.resultImage.configure(image=self.monsterImage)
        self.resultImage.image=self.monsterImage

        return filename

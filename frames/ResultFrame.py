import tkinter as tk
from Styles import *

class ResultFrame(tk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.configure(borderwidth=2, relief="groove", bg=TAN, bd=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def setPositions(self, resultLabel, resultImage, resultList):
        resultLabel.grid(column=0, row=0, sticky=tk.S)
        resultImage.grid(column=0, row=1, sticky=tk.N)
        resultList.grid(column=0, row=2, sticky=tk.S)

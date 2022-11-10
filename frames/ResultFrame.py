import tkinter as tk
from Styles import *

class ResultFrame(tk.Frame):

    def __init__(self, container):
        super().__init__(container)

        self.configure(borderwidth=2, relief="groove", bg=TAN, bd=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def setPositions(self, resultLabel, resultDesc, resultImage, resultList):
        resultLabel.grid(column=0, row=0, sticky=tk.S, pady = (10, 10))
        resultDesc.grid(column=0, row=1, sticky=tk.S, pady = (10, 10))
        resultImage.grid(column=0, row=2, sticky=tk.N, pady = (10, 10))
        resultList.grid(column=0, row=3, sticky=tk.S, pady = (10, 10))

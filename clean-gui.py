import tkinter as tk
from tkinter import StringVar, ttk
from turtle import left

def getNumCharactersStr(var, index, mode) -> str:
    print("variable: " + var.get())
    return var
    

# Main window properties
window = tk.Tk()
window.geometry("700x500")
window.title("DnD Monster Generator")

# Top title
ttk.Label(
    window, 
    text="DnD Monster Generator",
    font=('Arial', 30, 'bold')
).pack(ipady=20)

# Instructions info
ttk.Label(
    window,
    text="Welcome to the monster library.\nWe'll generate a monster based on your party and other factors.",
    font=('Arial', 14),
    justify=tk.CENTER
).pack()

# Create frame for non-character settings
nonCharacterFrame = tk.Frame(window)

ttk.Label(nonCharacterFrame, text='Number of characters: ').grid(column=0, row=0)

charText = tk.StringVar()
charText.trace_add("write", getNumCharactersStr)
numCharsEntry = ttk.Entry(nonCharacterFrame, width=5, textvariable=charText)
numCharsEntry.grid(column=1, row=0, padx=(0, 20))

ttk.Label(nonCharacterFrame, text='Terrain: ').grid(column=2, row=0)
ttk.Entry(nonCharacterFrame, width=20).grid(column=3, row=0, padx=(0, 20))

ttk.Label(nonCharacterFrame, text='Overall Difficulty: ').grid(column=4, row=0)
ttk.Entry(nonCharacterFrame, width=5).grid(column=5, row=0)

nonCharacterFrame.pack(pady=10)

# Character frame
characterFrame = tk.Frame(window)


numCharacters = 0
try:
    numCharacters = int(numCharsEntry.get())
except:
    numCharacters = 0

ttk.Label(characterFrame, text='Character').grid(column=0, row=0)
ttk.Label(characterFrame, text='Level').grid(column=1, row=0)
for i in range(1, numCharacters + 1):
    ttk.Entry(characterFrame, width=20).grid(column=0, row=i, padx=(0, 10), pady=5)
    ttk.Entry(characterFrame, width=5).grid(column=1, row=i)

characterFrame.pack(pady=10)


# Display window
window.mainloop()
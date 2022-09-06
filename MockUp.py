# Mock up of the monster generator
import requests
import json
import tkinter as tk

window = tk.Tk()
window.geometry("700x500")
window.title("Monster Generator")

label = tk.Label(
    window, text="Welcome to the monster library, please enter a party with the format class level for each member.")
label.pack()
classes = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
           "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]

variable1 = tk.StringVar(window)
dropDownMenu1 = tk.OptionMenu(window, variable1, *classes)
dropDownMenu1.pack(pady=10)
variable2 = tk.StringVar(window)
dropDownMenu2 = tk.OptionMenu(window, variable2, *classes)
dropDownMenu2.pack(pady=10)
variable3 = tk.StringVar(window)
dropDownMenu3 = tk.OptionMenu(window, variable3, *classes)
dropDownMenu3.pack(pady=10)
variable4 = tk.StringVar(window)
dropDownMenu4 = tk.OptionMenu(window, variable4, *classes)
dropDownMenu4.pack(pady=10)

result = tk.StringVar()
result.set("")


def button_action():
    response = requests.get("https://www.dnd5eapi.co/api/monsters/troll/")
    result.set(response.json().get('name'))


button = tk.Button(window, text='Get Monster', command=button_action)
button.pack(pady=10)

resultLabel = tk.Label(window, textvariable=result)
resultLabel.pack()

window.mainloop()

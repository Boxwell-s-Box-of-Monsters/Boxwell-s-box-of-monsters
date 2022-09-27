import tkinter as tk
import random
import requests
from styles import TAN, BLACK, FONT
from frames.character_frame import CharacterFrame
from frames.terrain_frame import TerrainFrame
from frames.damage_type_frame import DamageTypeFrame
from frames.description_frame import DescriptionFrame


############################
# Main Window
############################


# get_appropriate_cr
# Gets a list of monsters from the challenge rating
def get_appropriate_cr(character_list):
    challenge_rating = 0
    for character in character_list:
        challenge_rating += int(character['level'].get())
    challenge_rating /= 4
    return round(challenge_rating, 0)


# response_list_adapter
# Picks a best monster from the available list
def response_list_adapter(challenge_rating):
    # Get list of monsters
    response = requests.get(
        "https://www.dnd5eapi.co/api/monsters?challenge_rating=" + str(challenge_rating))
    return response.json().get('results')


# best_response_adapter
# Prints the current best monster
def best_response_adapter(response_list):
    # Later we will want to change this function based on elastic search
    random.seed(random.randint(0, 100))
    rand_idx = random.randint(0, len(response_list) - 1)
    return requests.get("https://www.dnd5eapi.co" + response_list[rand_idx]['url'])


# print_adapter
# Placeholder description
def print_adapter(response):
    # Create a string
    response_text = response.json().get('name')
    response_text += "\nHP: " + str(response.json().get('hit_points'))
    response_text += "\tAC: " + str(response.json().get('armor_class'))
    response_text += "\tCR: " + str(response.json().get('challenge_rating'))
    # New Line with Monster Stats
    response_text += "\nStr: " + str(response.json().get('strength'))
    response_text += "\tDex: " + str(response.json().get('dexterity'))
    response_text += "\tCon: " + str(response.json().get('constitution'))
    response_text += "\tInt: " + str(response.json().get('intelligence'))
    response_text += "\tWis: " + str(response.json().get('wisdom'))
    response_text += "\tCha: " + str(response.json().get('charisma'))
    return response_text


# MainWindow
# Placeholder description
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("325x610")
        self.title("Monster Generator")
        self.configure(bg=TAN)

        options = {'padx': 5, 'pady': 5}

        # Top Label
        label_text = "Welcome to the monster library, please enter the relevant information below."
        self.label = tk.Label(self, text= label_text, wraplength=300, justify="center", background=TAN,
                              font=(FONT, 10, "bold"), fg=BLACK)
        self.label.grid(column=0, row=0, **options)

        # Terrain Frame
        terrain_frame = TerrainFrame(self)
        terrain_frame.grid(column=0, row=1, sticky=tk.W, **options)

        # Characters Frame
        character_frame = CharacterFrame(self)
        character_frame.grid(column=0, row=2, sticky=tk.W, **options)

        # Damage Type Frame
        dmg_type_frame = DamageTypeFrame(self)
        dmg_type_frame.grid(column=0, row=3, sticky=tk.W, **options)

        # Description Frame
        descript_frame = DescriptionFrame(self)
        descript_frame.grid(column=0, row=4, sticky=tk.W, **options)

        # Get Monster Button and Result
        self.result = tk.StringVar()
        self.result.set("")

        self.button = tk.Button(self,
                                text='Get Monster',
                                command=lambda: self.handle_get_monster_button(
                                    character_frame.characters),
                                highlightbackground=TAN,
                                font=(FONT, 9, "bold"),
                                fg=BLACK)
        self.button.grid(column=0, row=6, sticky=tk.W, **options)

        # Print the result of the button
        self.result_label = tk.Label(self, textvariable=self.result, bg=TAN, font=(FONT, 10),
                                     fg=BLACK)
        self.result_label.grid(column=0, row=7)

    # Button Code
    def handle_get_monster_button(self, character_list):
        challenge_rating = self.get_appropriate_cr(character_list)
        response_list = response_list_adapter(challenge_rating)
        # Get top result
        if len(response_list) > 0:
            response = best_response_adapter(response_list)
            response_text = print_adapter(response)
        else:
            response_text = "Error, no monsters found"
        self.result.set(response_text)

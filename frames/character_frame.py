import tkinter as tk

from styles import BLACK, LIGHT, FONT


############################
# Character Frame
############################

class CharacterFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        self.configure(borderwidth=2, relief="groove", bg=LIGHT,
                       bd=0)

        # Character Container Label
        self.character_container_label = tk.Label(self,
                                                  text="Adventuring Party",
                                                  font=(FONT, 9, "bold"),
                                                  background=LIGHT,
                                                  fg=BLACK)
        self.character_container_label.grid(
            column=0, row=0, columnspan=3, **options)

        # Add/Remove Buttons
        self.add_character = tk.Button(self, text='Add Character', font=(FONT, 8),
                                       fg=BLACK, highlightbackground=LIGHT)
        self.remove_character = tk.Button(self, text="Remove Character", font=(FONT, 8),
                                          fg=BLACK, highlightbackground=LIGHT)
        self.add_character.grid(column=0, row=1, sticky=tk.W, **options)
        self.remove_character.grid(column=1, row=1, sticky=tk.W, **options)

        # Labels for Character table
        self.character_label = tk.Label(self, text="Character", bg=LIGHT, font=(FONT, 8, "bold"),
                                        fg=BLACK)
        self.lvl_label = tk.Label(self, text="Level", bg=LIGHT, font=(FONT, 8, "bold"),
                                  fg=BLACK)
        self.damage_label = tk.Label(self, text="Damage", bg=LIGHT, font=(FONT, 8, "bold"),
                                     fg=BLACK)
        self.character_label.grid(column=0, row=2, sticky=tk.W, **options)
        self.lvl_label.grid(column=1, row=2, sticky=tk.W, **options)
        self.damage_label.grid(column=2, row=2, sticky=tk.W, **options)

        # Drop down for dmg types
        char_type = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
                    "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
        # Characters
        self.characters = []
        for i in range(4):
            character_row = {}
            char_var = tk.StringVar(self)

            chr_drop_down = tk.OptionMenu(
                self, char_var, *char_type)
            chr_drop_down.config(width=int(self.winfo_width() / 2))
            chr_drop_down.grid(
                column=0, row=3 + i, sticky=tk.W, padx=5, pady=5)
            character_row['characterDrop'] = chr_drop_down
            character_row['character'] = char_var

            character_row['level'] = tk.Spinbox(self, from_=1, to=20)
            character_row['level'].grid(
                column=1, row=3 + i, sticky=tk.W, padx=5, pady=5)

            # character_row['Damage'] = tk.Label(
            #     characterContainer, text='Fire', font=(FONT, 8), bg=LIGHT)
            # character_row['Damage'].grid(
            #     column=2, row=3 + i, sticky=tk.W, padx=5, pady=5)

            self.characters.append(character_row)

from tkinter import *
from tkinter import ttk
from tkinter.font import Font

import top as top

combatant_list = []
player_list = []
turn_counter = 1

class Combatant:
    name = ""
    init_value = 0
    active = True
    turn_player = False

    def __init__(self, name, init_value):
        self.name = name
        self.init_value = init_value

    def __lt__(self, other):
        return self.init_value < other.init_value

def next_turn():
    global turn_counter
    print(f"Runde: {turn_counter}")
    turn_counter += 1
    player = combatant_list[0]
    #player.turn_player = True
    #print_combatant_list()
    #player.turn_player = False
    combatant_list.pop(0)
    combatant_list.append(player)
    update_listbox()


def create_team():
    jason = Combatant("Jason", 35)
    player_list.append(jason)
    koju = Combatant("Koju", 34)
    player_list.append(koju)
    kygia = Combatant("Kygia",33)
    player_list.append(kygia)
    mojo = Combatant("Mojo", 32)
    player_list.append(mojo)
    grendl = Combatant("Grendl", 31)
    player_list.append(grendl)
    kutora = Combatant("Kutora", 30)
    player_list.append(kutora)
    global combatant_list
    combatant_list = player_list

def add_player():
    player = Combatant(name_entry.get(), int(init_entry.get()))
    init_entry.delete(0,END)
    name_entry.delete(0,END)
    combatant_list.append(player)
    update_listbox()

def sort_players():
    # sort list
    combatant_list.sort()
    combatant_list.reverse()
    update_listbox()

def edit():
    edit_player = combatant_list[listbox.curselection()[0]]
    edit_player.init_value = int(init_entry.get())
    if name_entry.get():
        edit_player.name = name_entry.get()
    init_entry.delete(0,END)
    name_entry.delete(0,END)
    sort_players()

def remove_player():
    combatant_list.pop(listbox.curselection()[0])
    update_listbox()

def update_listbox():
    listbox.delete(0, END)
    for element in combatant_list:
        listbox.insert(END, str(element.init_value) + " " + element.name)
    listbox.itemconfig(0, bg="cyan", fg="green")


def print_combatant_list():
    for element in combatant_list:
        if element.turn_player:
            print(f"*[{element.init_value} - {element.name}]")
        else:
            print(f"{element.init_value} - {element.name}")

if __name__ == "__main__":
    # fill up list with hardcoded team members
    create_team()

    # gui
    dark_mode = True
    window = Tk()
    window.title("Initiative Tracker")
    window.geometry("620x330")
    font_b = Font(size=12)
    font_bb = Font(size=14)
    listbox = Listbox(window, height=10, font=font_bb,exportselection=False)
    for element in player_list:
        listbox.insert(END, str(element.init_value) + " " + element.name)

    listbox.pack(fill=X, padx=15, pady=10)

    name_label = Label(window, text="Name:", height=1)
    name_label.pack(padx=(15, 5), pady=5, side=LEFT)

    name_entry = Entry(window, width=8)
    name_entry.pack(padx=5, pady=5, side=LEFT)

    init_label = Label(window, text="Init:")
    init_label.pack(padx=5, pady=5, side=LEFT)

    init_entry = Entry(window, width=5)
    init_entry.pack(padx=5, pady=5, side=LEFT)

    add_button = Button(text="+", command=add_player, height=1, width=4, font=font_bb)
    add_button.pack(padx=5, pady=5, side=LEFT)

    remove_button = Button(text="-", command=remove_player, height=1, width=4, font=font_bb)
    remove_button.pack(padx=5, pady=5, side=LEFT)

    edit_button = Button(text="EDIT", command=edit, height=1, width=4, font=font_bb)
    edit_button.pack(padx=5, pady=5, side=LEFT)

    start_button = Button(text="SORT", command=sort_players, height=1, width=4, font=font_bb)
    start_button.pack(padx=5, pady=5, side=LEFT)

    next_button = Button(text="NEXT", command=next_turn, height=1, width=4, font=font_bb)
    next_button.pack(padx=5, pady=5, side=LEFT)

    if dark_mode:
        window.configure(background="black")

    update_listbox()

    window.mainloop()

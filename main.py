from tkinter import *
from tkinter.font import Font

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
    # player.turn_player = True
    # print_combatant_list()
    # player.turn_player = False
    combatant_list.pop(0)
    combatant_list.append(player)
    update_listbox()


def create_team():
    content = open("input").readlines()
    for x in range(0, len(content)):
        new_combatant = Combatant(content[x].rstrip(), 0)
        player_list.append(new_combatant)
    global combatant_list
    combatant_list = player_list


def add_player():
    player = Combatant(name_entry.get(), int(init_entry.get()))
    init_entry.delete(0, END)
    name_entry.delete(0, END)
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
    init_entry.delete(0, END)
    name_entry.delete(0, END)
    sort_players()


def remove_player():
    combatant_list.pop(listbox.curselection()[0])
    update_listbox()


def update_listbox():
    listbox.delete(0, END)
    for element in combatant_list:
        listbox.insert(END, str(element.init_value) + " " + element.name)
    listbox.itemconfig(0, bg="cyan", fg="red")


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
    window.geometry("400x340")
    font_b = Font(size=12)
    font_bb = Font(size=14)
    listbox = Listbox(window, height=10, font=font_bb, exportselection=False)
    for element in player_list:
        listbox.insert(END, str(element.init_value) + " " + element.name)


    scrollbar = Scrollbar(window, orient=VERTICAL)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    listbox.grid(row=0, column=0, rowspan=4,
                 columnspan=2, sticky=N + E + S + W, padx=(10, 0), pady=10)
    listbox.columnconfigure(0, weight=1)

    scrollbar.grid(row=0, column=2, rowspan=4, sticky=N + S, padx=(0, 10), pady=10)

    next_button = Button(text="NEXT", command=next_turn, height=3, width=8, font=font_bb)
    next_button.grid(row=1, column=3, sticky=EW, padx=10, pady=10)

    name_label = Label(window, text="Name:", height=1, width=5)
    name_label.grid(row=4, column=0, sticky=W, padx=(10, 0))

    name_entry = Entry(window, width=8)
    name_entry.grid(row=4, column=0, padx=(35, 0), pady=10)

    init_label = Label(window, text="Init:", height=1, width=5)
    init_label.grid(row=5, column=0, sticky=W, padx=(10, 0))

    init_entry = Entry(window, width=8)
    init_entry.grid(row=5, column=0, padx=(35, 0), pady=10)

    add_button = Button(text="+", command=add_player, height=1, width=4)
    add_button.grid(row=4, column=1,sticky=W, padx=(0, 0))

    remove_button = Button(text="-", command=remove_player, height=1, width=4)
    remove_button.grid(row=5, column=1, sticky=W, padx=(0, 0))

    edit_button = Button(text="EDIT", command=edit, height=1, width=4)
    edit_button.grid(row=4, column=1, sticky=E, padx=(0, 0))

    sort_button = Button(text="SORT", command=sort_players, height=1, width=4)
    sort_button.grid(row=5, column=1, sticky=E, padx=(0, 0))

    if dark_mode:
        window.configure(background="lightgrey")

    update_listbox()

    window.mainloop()

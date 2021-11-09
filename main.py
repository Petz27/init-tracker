from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from enum import Enum
from tkinter.messagebox import showinfo

from PIL import ImageTk, Image

combatant_list = []
player_list = []
turn_counter = 1

class BGColor(Enum):
    BG_Image = 0
    Dark_Mode = 1
    Bright_Mode = 2
    Modern = 3

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
    #print(f"Runde: {turn_counter}")
    turn_counter += 1
    player = combatant_list[0]
    # player.turn_player = True
    # print_combatant_list()
    # player.turn_player = False
    combatant_list.pop(0)
    combatant_list.append(player)
    update_listbox()
    #print(str(tree.index(0)[1]))
    #tree.insert("", END, values=(tree[0][0], tree[0][1]))


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

    # add to tree
    tree.insert("", END, values=(player.init_value, player.name))


def sort_players():
    # sort list
    combatant_list.sort()
    combatant_list.reverse()
    update_listbox()

    # sort treeview
    treeview_sort_column(tree, tree.column("init"), False)

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
               treeview_sort_column(tv, col, not reverse))


def edit():
    edit_player = combatant_list[listbox.curselection()[0]]
    edit_player.init_value = int(init_entry.get())
    if name_entry.get():
        edit_player.name = name_entry.get()
    init_entry.delete(0, END)
    name_entry.delete(0, END)
    sort_players()


def remove_player():
    selected = tree.focus()
    print(tree.item(selected, 'values')[1])
    tree.delete(tree.focus())

    print(listbox.curselection()[0])
    combatant_list.pop(listbox.curselection()[0])
    update_listbox()


def update_listbox():
    listbox.delete(0, END)
    for element in combatant_list:
        listbox.insert(END, str(element.init_value) + " " + element.name)
    listbox.itemconfig(0, bg="blue", fg="white")


def print_combatant_list():
    for element in combatant_list:
        if element.turn_player:
            print(f"*[{element.init_value} - {element.name}]")
        else:
            print(f"{element.init_value} - {element.name}")


if __name__ == "__main__":
    # fill up list with names from input file
    create_team()

    # gui
    change_background = BGColor.Modern

    window = Tk()
    path = "res/wood.jpg"
    filename = ImageTk.PhotoImage(Image.open(path))
    if change_background == BGColor.BG_Image:
        background_label = Label(window, image=filename)
        background_label.place(x=0, y=0)
    elif change_background == BGColor.Dark_Mode:
        window.configure(background="#3B4A4C")
    elif change_background == BGColor.Bright_Mode:
        window.configure(background="#D6E1F4")
    elif change_background == BGColor.Modern:
        window.configure(background="#3679AD")

    window.title("Initiative Tracker")
    window.geometry("600x440")
    window.iconbitmap("res/d20.ico")
    font_b = Font(size=12)
    font_lb = Font(size=14)


    listbox = Listbox(window, bg="#9B95A1", height=10, font=font_lb, exportselection=False)
    for element in player_list:
        listbox.insert(END, str(element.init_value) + " " + element.name)

    scrollbar = Scrollbar(window, orient=VERTICAL)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    listbox.grid(row=0, column=0, rowspan=4,
                 columnspan=2, sticky=N + E + S + W, padx=(10, 0), pady=10)
    listbox.columnconfigure(0, weight=1)

    scrollbar.grid(row=0, column=2, rowspan=4, sticky=N + S, padx=(0, 10), pady=10)



    # tree
    columns = ('init', 'char_name')

    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.column("init", minwidth=20, width=50, stretch=NO, anchor=CENTER)
    tree.column("char_name", minwidth=50, width=100, stretch=NO, anchor=CENTER)
    # define headings
    tree.heading('init', text='Value')
    tree.heading('char_name', text='Character')

    # add data to the treeview
    for n in player_list:
        tree.insert("", END, values=(str(n.init_value), n.name))

    tree.grid(row=0, column=8, sticky='nsew', pady=10)

    # add a scrollbar
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=9, sticky='ns', pady=10)



    # next button needed to skip the selection to the next player
    next_button = Button(text="NEXT", bg="#9B95A1", command=next_turn, height=3, width=8, font=font_lb)
    next_button.grid(row=1, column=3, sticky=EW, padx=10, pady=10)

    name_label = Label(window, text="Name:", height=1, width=5)
    name_label.grid(row=4, column=0, sticky=W, padx=(10, 0))

    name_entry = Entry(window, width=8)
    name_entry.grid(row=4, column=0, padx=(35, 0), pady=10)

    init_label = Label(window, text="Init:", height=1, width=5)
    init_label.grid(row=5, column=0, sticky=W, padx=(10, 0))

    init_entry = Entry(window, width=8)
    init_entry.grid(row=5, column=0, padx=(35, 0), pady=10)

    add_button = Button(text="+", bg="#9B95A1", command=add_player, height=1, width=4)
    add_button.grid(row=4, column=1, sticky=W, padx=(0, 0))

    remove_button = Button(text="-", bg="#9B95A1", command=remove_player, height=1, width=4)
    remove_button.grid(row=5, column=1, sticky=W, padx=(0, 0))

    edit_button = Button(text="EDIT", bg="#9B95A1", command=edit, height=1, width=4)
    edit_button.grid(row=4, column=1, sticky=E, padx=(0, 0))

    sort_button = Button(text="SORT", bg="#9B95A1", command=sort_players, height=1, width=4)
    sort_button.grid(row=5, column=1, sticky=E, padx=(0, 0))

    update_listbox()

    window.mainloop()

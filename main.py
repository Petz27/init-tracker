from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from enum import Enum
from PIL import ImageTk, Image

player_list = []
window_size = "500x400"


class BGColor(Enum):
    BG_Image = 0
    Dark_Mode = 1
    Bright_Mode = 2
    Modern = 3


class Combatant:
    name = ""
    init_value = 0

    def __init__(self, name, init_value):
        self.name = name
        self.init_value = init_value

    def __lt__(self, other):
        return self.init_value < other.init_value


def recolor_first():
    tree.item(tree.get_children()[0], tags="first")
    tree.tag_configure("first", background="blue", foreground="white", font=(None, 15))


def next_turn():
    kids = tree.get_children()
    player = tree.item(kids[0], "values")
    tree.insert("", END, values=(player[0], player[1]))
    tree.delete(kids[0])
    recolor_first()


def create_team():
    content = open("input").readlines()
    for x in range(0, len(content)):
        new_combatant = Combatant(content[x].rstrip(), 0)
        player_list.append(new_combatant)


def add_player():
    name = name_entry.get()
    value = int(init_entry.get())
    init_entry.delete(0, END)
    name_entry.delete(0, END)
    # add to tree
    tree.insert("", END, values=(value, name))


def remove_player():
    selected = tree.focus()
    print(tree.item(selected, 'values')[1])
    tree.delete(tree.focus())


def edit_player():
    selected = tree.focus()
    print(tree.item(selected, 'values')[0])

    if name_entry.get():
        new_name = name_entry.get()
        tree.item(selected, values=(tree.item(selected, 'values')[0], new_name))

    if init_entry.get():
        new_value = int(init_entry.get())
        tree.item(selected, values=(new_value, tree.item(selected, 'values')[1]))


def sort_players():
    tree.item(tree.get_children()[0], tags="-")
    tree.tag_configure("-", background="white", foreground="black", font=font_tree)
    # sort treeview
    l = [(tree.set(k, "Value"), k) for k in tree.get_children('')]
    l.sort(key=lambda t: int(t[0]), reverse=True)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    recolor_first()


def configure_background():
    # gui background
    change_background = BGColor.Modern
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


def configure_treeview():
    # treeview
    tree.column("Value", minwidth=20, width=100, stretch=NO, anchor=CENTER)
    tree.column("char_name", minwidth=50, width=160, stretch=NO, anchor=CENTER)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=(None, 14))
    style.configure("Treeview", rowheight=25, font=font_tree)

    # define headings
    tree.heading('Value', text='Value')
    tree.heading('char_name', text='Character')
    tree.grid(row=0, column=0, rowspan=4, columnspan=2, sticky=N + E + S + W, padx=(10, 0), pady=10)

    # add data to the treeview
    for n in player_list:
        tree.insert("", END, values=(int(n.init_value), n.name))
    recolor_first()

    # add a scrollbar
    scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=2, rowspan=4, sticky='ns', pady=10)


def configure_entries():
    name_label = Label(window, text="Name:", height=1, width=5)
    name_label.grid(row=4, column=0, sticky=W, padx=(10, 0))

    init_label = Label(window, text="Init:", height=1, width=5)
    init_label.grid(row=5, column=0, sticky=W, padx=(10, 0))

    name_entry.grid(row=4, column=0, padx=(35, 0), pady=10)
    init_entry.grid(row=5, column=0, padx=(35, 0), pady=10)


def create_buttons():
    # next button needed to skip the selection to the next player
    next_button = Button(text="NEXT", bg="#e0e0e0", command=next_turn, height=3, width=8, font=font_lb)
    next_button.grid(row=1, column=3, sticky=EW, padx=60, pady=10)

    add_button = Button(text="+", bg="#9B95A1", command=add_player, height=1, width=4)
    add_button.grid(row=4, column=1, sticky=W, padx=(0, 0))

    remove_button = Button(text="-", bg="#9B95A1", command=remove_player, height=1, width=4)
    remove_button.grid(row=5, column=1, sticky=W, padx=(0, 0))

    edit_button = Button(text="EDIT", bg="#9B95A1", command=edit_player, height=1, width=4)
    edit_button.grid(row=4, column=1, sticky=E, padx=(0, 0))

    sort_button = Button(text="SORT", bg="#9B95A1", command=sort_players, height=1, width=4)
    sort_button.grid(row=5, column=1, sticky=E, padx=(0, 0))


if __name__ == "__main__":
    # fill up list with names from input file
    create_team()

    window = Tk()
    window.title("Initiative Tracker")
    window.geometry(window_size)
    window.iconbitmap("res/d20.ico")

    font_lb = Font(size=14)
    font_tree = Font(size=12)

    # set up background color/image
    configure_background()

    # treeview used to show player names and initiative value in GUI
    columns = ('Value', 'char_name')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    configure_treeview()

    name_entry = Entry(window, width=8)
    init_entry = Entry(window, width=8)

    # set up all labels and configures entries needed in GUI
    configure_entries()

    # set up all buttons needed in GUI
    create_buttons()

    window.mainloop()

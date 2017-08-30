import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import pyHook
from main import OnKeyboardEvent as Oke
import tkSimpleDialog

Q = 0x10
W = 0x11
E = 0x12
R = 0x13
D = 0x20
F = 0x21
Z = 0x2C
X = 0x2D
C = 0x2E
V = 0x2F
B = 0x30
P = 0x19
TAB = 0x0F
SPACE = 0x39


show_something = False
SKILL_1 = Q
SKILL_2 = W
SKILL_3 = E
SKILL_4 = R
SKILL_5 = D
SKILL_6 = F

ITEM_1 = Z
ITEM_2 = X
ITEM_3 = C
ITEM_4 = V
ITEM_5 = B
ITEM_6 = SPACE


class TestingGui(tk.Tk):
    def __init__(self):
        super().__init__()
        global show_something
        show_something = tk.BooleanVar()
        # self.show_something.set(True)
        self.title("Dota 2 hotkeys")
        self.geometry("500x300")
        self.resizable(False, False)

        style = ttk.Style()
        style.configure("TLabel", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
        style.configure("B.TLabel", font=(None, 40))
        style.configure("B.TButton", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
        style.configure("TEntry", foregound="black", background="white")

        self.menubar = tk.Menu(self)
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label='dummy', compound='left', command=dummy_callback)
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        edit_menu.add_checkbutton(label='show something', variable=show_something, command=self.show_somethingfunc)
        self.menubar.add_cascade(label='File', menu=file_menu)
        self.menubar.add_cascade(label='Edit', menu=edit_menu)
        self.configure(menu=self.menubar)

        shortcut_bar = tk.Frame(self, height=25, background='light sea green')
        shortcut_bar.pack(expand='no', fill='x')

        self.skill_1_button = tk.Button(self, text="skill 1", command=self.button_callback)
        self.skill_1_button.pack()

    def greet(self):
        print("Greetings!")

    def show_somethingfunc(self):
        global show_something
        # show_something = self.show_something.get()
        print("here")

    def button_callback(self):
        d = myDialog(self)


def dummy_callback():
    print("dummy!")


def OnKeyboardEvent(event):
    print("show something = ", show_something.get())
    print(event.Key)
    Oke(event)
    return True

e1 = 0


class myDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        global e1
        tk.Label(master, text="First:").grid(row=0)

        e1 = tk.Entry(master)
        e1.grid(row=0, column=1)
        return e1  # initial focus

    # def apply(self):
    #     first = e1.get()
    #     print("first = ", first)
    #     pass


# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse event
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()


gui = TestingGui()
try:
    gui.mainloop()
except KeyboardInterrupt:
    # quit_event.set()
    pass
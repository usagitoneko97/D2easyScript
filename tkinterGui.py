import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import pyHook
from main import OnKeyboardEvent as Oke

show_something = False

class testing_gui(tk.Tk):
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

    def greet(self):
        print("Greetings!")

    def show_somethingfunc(self):
        global show_something
        # show_something = self.show_something.get()
        print("here")


def dummy_callback():
    print("dummy!")


def OnKeyboardEvent(event):
    print("show something = ", show_something.get())
    print(event.Key)
    Oke(event)
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse event
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()


gui = testing_gui()
try:
    gui.mainloop()
except KeyboardInterrupt:
    # quit_event.set()
    pass
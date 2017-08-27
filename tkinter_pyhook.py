from tkinter import *
import threading

import pythoncom, pyHook

from multiprocessing import Pipe
from multiprocessing import Queue
import functools

class TestingGUI:
    def __init__(self, root, queue, quitfun):
        self.root = root
        self.root.title('TestingGUI')
        self.queue = queue
        self.quitfun = quitfun

        self.button = Button(root, text="Withdraw", command=self.hide)
        self.button.grid()

        self.search = StringVar()
        self.searchbox = Label(root, textvariable=self.search)
        self.searchbox.grid()

        self.root.bind('<<pyHookKeyDown>>', self.on_pyhook)
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

        self.hiding = False

    def hide(self):
        if not self.hiding:
            print ('hiding')
            self.root.withdraw()
            # instead of time.sleep + self.root.deiconify()
            self.root.after(2000, self.unhide)
            self.hiding = True

    def unhide(self):
        self.root.deiconify()
        self.hiding = False

    def on_quit(self):
        self.quitfun()
        self.root.destroy()

    def on_pyhook(self, event):
        if not queue.empty():
            scancode, ascii = queue.get()
            print (scancode, ascii)
            if scancode == 82:
                self.hide()

            self.search.set(ascii)

root = Tk()
pread, pwrite = Pipe(duplex=False)
queue = Queue.Queue()

def quitfun():
    pwrite.send('quit')

TestingGUI = TestingGUI(root, queue, quitfun)

def hook_loop(root, pipe):
    while 1:
        msg = pipe.recv()

        if type(msg) is str and msg == 'quit':
            print ('exiting hook_loop')
            break

        root.event_generate('<<pyHookKeyDown>>', when='tail')

# functools.partial puts arguments in this order
def keypressed(pipe, queue, event):
    queue.put((event.ScanCode, chr(event.Ascii)))
    pipe.send(1)
    return True

t = threading.Thread(target=hook_loop, args=(root, pread))
t.start()

hm = pyHook.HookManager()
hm.HookKeyboard()
hm.KeyDown = functools.partial(keypressed, pwrite, queue)

try:
    root.mainloop()
except KeyboardInterrupt:
    quit_event.set()
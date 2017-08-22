import pythoncom
import pyHook
from sendKeysTest import PressKey, ReleaseKey
import time


def OnKeyboardEvent(event):
    print(event.Key)
    if event.Key == 'Add':
        print("here")
        print("event key: ", event.Key)
        PressKey(0x11)
        ReleaseKey(0x11)
# return True to pass the event to other handlers
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse event
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever

pythoncom.PumpMessages()

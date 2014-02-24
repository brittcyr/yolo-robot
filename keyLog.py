from Xlib.display import Display
import Xlib
from Xlib import X
import Xlib.XK
import sys
import signal
import time
display = None
root = None

def handle_event(event):
    print "handle!"
    if (event.type == X.KeyRelease):
        send_key("x")

# from http://shallowsky.com/software/crikey/pykey-0.1
def send_key(emulated_key):
    shift_mask = 0 # or Xlib.X.ShiftMask
    window = display.get_input_focus()._data["focus"]
    keysym = Xlib.XK.string_to_keysym(emulated_key)
    keycode = display.keysym_to_keycode(keysym)
    event = Xlib.protocol.event.KeyPress(
        time = int(time.time()),
        root = root,
        window = window,
        same_screen = 0, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = shift_mask,
        detail = keycode
        )
    window.send_event(event, propagate = True)
    event = Xlib.protocol.event.KeyRelease(
        time = int(time.time()),
        root = display.screen().root,
        window = window,
        same_screen = 0, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = shift_mask,
        detail = keycode
        )
    window.send_event(event, propagate = True)

def main():
    # current display
    global display,root
    display = Display()
    root = display.screen().root

    # we tell the X server we want to catch keyPress event
    root.change_attributes(event_mask = X.KeyPressMask|X.KeyReleaseMask)
    # just grab the "1"-key for now
    root.grab_key(10, 0, True,X.GrabModeSync, X.GrabModeSync)

    signal.signal(signal.SIGALRM, lambda a,b:sys.exit(1))
    signal.alarm(10)
    while 1:
        print 'waiting'
        event = display.next_event()
        print "event"
        handle_event(event)
        display.allow_events(X.AsyncKeyboard, X.CurrentTime)

if __name__ == '__main__':
    main()

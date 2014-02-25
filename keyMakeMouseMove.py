from Xlib.display import Display
from Xlib import X
import Xlib.XK
import Xlib.ext.xtest
import sys
import signal
import time

display = None
root = None

def handle_event(event):
    if (event.type == X.KeyRelease):
        send_key("x")

def send_key(emulated_key):
    shift_mask = 0 # or Xlib.X.ShiftMask
    window = display.get_input_focus()._data["focus"]
    keysym = Xlib.XK.string_to_keysym(emulated_key)
    keycode = display.keysym_to_keycode(keysym)

    # send the key
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

    # Move the mouse
    root.warp_pointer(500, 475)

    # Click the mouse
    Xlib.ext.xtest.fake_input(display,Xlib.X.ButtonPress, 1)
    Xlib.ext.xtest.fake_input(display,Xlib.X.ButtonRelease, 1)
    display.sync()

    # We switched windows
    window = display.get_input_focus()._data["focus"]

    # Type the letter keycode into the new window
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
    root.grab_key(10, 0, True, X.GrabModeSync, X.GrabModeSync)

    root.grab_button(1, X.Mod1Mask, 1, X.ButtonPressMask,
                    X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE)

    # only run for 10 seconds
    signal.signal(signal.SIGALRM, lambda a,b:sys.exit(1))
    signal.alarm(10)

    while 1:
        # Handle events without blocking
        event = display.next_event()
        handle_event(event)
        display.allow_events(X.AsyncKeyboard, X.CurrentTime)

if __name__ == '__main__':
    main()

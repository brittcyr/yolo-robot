import Xlib
import Xlib.display
display = Xlib.display.Display(':0')
root = display.screen().root
root.change_attributes(event_mask=
    Xlib.X.ButtonPressMask | Xlib.X.ButtonReleaseMask)
while True:
    event = root.display.next_event()
    print "Hello button press"

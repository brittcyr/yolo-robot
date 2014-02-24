from Xlib.display import Display
from Xlib import X

# custom keys from my dell D400 Laptop
vol_plus  = 176
vol_moins = 174

keys = [vol_plus,vol_moins]

def changeVolume(aValue):
    return
#	mixer = oss.open_mixer()
#	symbol = oss.SOUND_DEVICE_LABELS.index('Vol  ')
#	left,right  = mixer.read_channel(symbol)

#	avg = (left + right) / 2
#	if (avg + aValue) >= 0:
#		mixer.write_channel(symbol,(left + aValue,right + aValue))
#	mixer.close()

def handle_event(aEvent):
    keycode = aEvent.detail
    print aEvent
    if aEvent.type == X.KeyPress:
		if keycode == vol_moins:
			changeVolume(-2)
		elif keycode == vol_plus:
			changeVolume(+2)

def main():
	# current display
	disp = Display()
	root = disp.screen().root

	# we tell the X server we want to catch keyPress event
	root.change_attributes(event_mask = X.KeyPressMask)

	for keycode in keys:
		root.grab_key(keycode, X.AnyModifier, 1,X.GrabModeAsync, X.GrabModeAsync)

    while 1:
        event = root.display.next_event()
        print 'test'
        handle_event(event)

if __name__ == '__main__':
	main()

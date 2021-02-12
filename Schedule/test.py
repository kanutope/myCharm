from Tkinter import *

def printKey (evnt):
	print evnt.keysym + " - " + str(evnt.keycode) + " -> " + str(evnt.keysym_num)

def printButton (evnt):
	print "state=" + format(evnt.state, "0>4x") + "  x,y=" + str(evnt.x) + "," + str(evnt.y) + "  root x,y=" + str(evnt.x_root) + "," + str(evnt.y_root)

root = Tk()
frame1 = Frame(root)
frame2 = Frame(root)

frame2.pack( )					# side = BOTTOM )
frame1.pack( after = frame2)

bluebutton = Button(frame1, text="Blue", fg="blue")
bluebutton.pack( side = LEFT )

greenbutton = Button(frame1, text="Brown", fg="brown")
greenbutton.pack( side = LEFT )

redbutton = Button(frame1, text="Red", fg="red")
redbutton.pack( side = LEFT)

blackbutton = Button(frame2, text="Black", fg="black")
blackbutton.pack( side = BOTTOM)

root.bind_all('<KeyPress>', printKey)
root.bind_all('<Button>',   printButton)

root.mainloop()

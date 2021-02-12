import os
import sys

import Tkinter as tk

execDir = os.path.dirname(sys.argv[0])
if len(execDir) == 0: execDir = "."
	
print "execDir = ["+execDir+"]"

# proc's one may need
import nspace
import procs
import drag
import schedule		# formerly called 'file'
import event
import objects

# clean it up! For restarting purpose.
procs.exiting

# create top window
wdwRoot = tk.Tk()		#  class instantiated to create a toplevel widget of Tk which usually is the main window
wdwRoot.title("Schedule Management")
wdwWork = objects.frmWork(master=wdwRoot)

wdwRoot.mainloop()


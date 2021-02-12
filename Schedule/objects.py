import Tkinter      as tk
import ttk			as ttk
import ScrolledText as st

class frmInput(ttk.Frame):
	# frmLog is inherited from class 'Frame'
	# Tk - frame pathName ?options?
	
	def setWidgets(self):
		self.wdgEntry = ttk.Entry(self, textvariable=self.input, width=24)
		self.wdgEntry.grid(row=0)

		self.wdgClear = tk.Button(self, text="Cancel", command=self.cancel)
		self.wdgClear.grid(row=1, sticky=tk.W)

	def cancel(self):
		self.input = ""
		self.wdgEntry.delete(0, tk.END)
		self.parent.withdraw()

	def getInput(self):
		self.parent.deiconify()

	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.parent = master
		self.input = ""
		
		self.grid()
		self.setWidgets()

class frmLog(ttk.Frame):
	# frmLog is inherited from class 'Frame'
	# Tk - frame pathName ?options?
	def setWidgets(self):
		self.wdgLog = st.ScrolledText(self, height=5)
		self.wdgLog.grid(row=0)

		self.wdgClear = tk.Button(self, text="Clear", command=self.clear)
		self.wdgClear.grid(row=1, sticky=tk.W)

	def append(self, Str):
		self.wdgLog.insert(tk.END, Str + '\n')	# , tags=None)

	def clear(self):
		self.wdgLog.delete(1.0, tk.END)

	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.grid()
		self.setWidgets()

class frmWork(ttk.Frame):
	def __scrollHorizontal(self, *L):
		op, step = L[0], L[1]
		
		if op == 'scroll':
			unit = L[2]
			self.scrollFrame.xview_scroll(step, unit)
		elif op == 'moveto':
			self.scrollFrame.xview_moveto(step)
			
	def __scrollVertical(self, *L):
		op, step = L[0], L[1]
		
		if op == 'scroll':
			unit = L[2]
			self.scrollFrame.yview_scroll(step, unit)
		elif op == 'moveto':
			self.scrollFrame.yview_moveto(step)
			
	# create a new Schedule
	def newSchedule(self):
		self.frmLog.append("newSchedule")
		self.wdwInput.deiconify()
		# proc newSchedule {win} {
		#   if {[getstring::tk_getString $win.gs nam "New schedule"]} {
		#     if {[lsearch -exact $::cnvs $nam]==-1} {
		#       return [createSchedule $nam]
		#    } else {
		#       tk_messageBox					\
		#       	-icon warning					\
		#       	-message "Schedule $nam already exist!"	\
		# 	-parent $win					\
		# 	-title "Already exist"				\
		# 	-type ok
		#       return ""
		#    }
		#  }
		# }
		
	def setMenu(self):
		self.menuFile = tk.Menubutton(self, text="File")
		self.menuFile.grid(row=0, column=0, sticky=tk.W)

		self.menuFile.subMenu = tk.Menu(self.menuFile)
		self.menuFile['menu'] = self.menuFile.subMenu

		self.menuFile.subMenu.add('command', label='New' , accelerator="Cmd-N", underline="0", command=self.newSchedule)
		self.menuFile.subMenu.add('command', label='Quit', accelerator="Cmd-Q", underline="0", command= self.winfo_toplevel().quit)
		
		self.bind('<Meta-Key-n>', self.winfo_toplevel().quit)

	def setWidgets(self):
		self.horizScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.__scrollHorizontal)
		self.horizScroll.grid(row=1, sticky=tk.W+tk.E)

		self.scrollFrame = tk.Canvas(self, width=608, height=480)
		self.scrollFrame.grid(row=2, column=0)
		
		self.vertiScroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.__scrollVertical)
		self.vertiScroll.grid(row=2, column=1, sticky=tk.N+tk.S)
		
		self.scrollFrame['xscrollcommand'] = self.horizScroll.set
		self.scrollFrame['yscrollcommand'] = self.vertiScroll.set

		self.statusBar = tk.Text(self, height=1)
		self.statusBar.insert(tk.END, "--- statusbar ---")
		self.statusBar.grid(row=3, sticky=tk.W+tk.E)
		
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)

		# elaborate master window
		master.borderwidth = 2
		master.relief = tk.RAISED

		# add menu to master window
		# self.menuFile = tk.Menu(master)
		# master['menu'] = self.menuFile
		
		self.grid(stick=tk.N+tk.E+tk.S+tk.W)
		self.setMenu()
		self.setWidgets()
		
		# create wdwLog window
		self.wdwLog = tk.Toplevel(master=self)
		self.wdwLog.title("Log")
		self.frmLog = frmLog(master=self.wdwLog)

		# create input window
		self.wdwInput = tk.Toplevel(master=self)
		self.wdwInput.title("Input")
		self.wdwInput.withdraw()
		self.frmInput = frmInput(master=self.wdwInput)
		
		self.frmLog.append("Frame created")

		
#	# create main window
#	proc createWork {} {
#	  set main [toplevel .main	\
#		-borderwidth 2		\
#		-relief raised		\
#		]
#	
#	  wm title .main "Schedule Management"
#	
#	# create topframe
#	  set top [MainFrame $main.topFrame	\
#	  	-textvariable ::mainStatus	\
#		-menu {
#			"Menu" {} m0 False {
#			{command "&New" {}
#				"Create a new Schedule" {Ctrl n} -command {
#				newSchedule $work
#				$work yview moveto 1}}
#			{command "E&xit" {}
#				"Close this window" {Ctrl x} -command {
#				exiting}}
#			}
#		   }]
#	
#	  $top showstatusbar status
#	  # pack $top -expand yes -fill both
#	  grid $top -sticky {n e s w}
#	
#	# create scrollable frame
#	  set frm [$top getframe]
#	  set ::sbx [scrollbar $frm.scrollBarX	\
#		-orient horizontal			\
#	  	-command {scrollChilds}		\
#		]
#	
#	  set work [ScrollableFrame $frm.workSpace	\
#	 	-width  608				\
#	 	-height 480				\
#		-yscrollcommand {$::sby set}		\
#	 	]
#	
#	  set ::sby [scrollbar $frm.scrollBarY	\
#		-orient vertical			\
#		-command {$work yview}		\
#		]
#	
#	  grid $::sbx -row 0 -column 0 -sticky {e w}
#	  grid $work  -row 1 -column 0 -sticky {n s}
#	  grid $::sby -row 1 -column 1 -sticky {n s}
#	
#	  return $work
#	}


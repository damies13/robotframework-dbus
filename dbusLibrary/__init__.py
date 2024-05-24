
from .dbusBase import dbusBase
from .dbudGnome import dbudGnome


from robot.api.deco import keyword, library


@library
class dbusLibrary:
	"""robotframework-dbus

	A Robot Framework library to help automation of linux desktop applications

	https://unix.stackexchange.com/questions/399753/how-to-get-a-list-of-active-windows-when-using-wayland
	Sadly, this no longer works on Gnome 41 for security reasons (https://www.reddit.com/r/gnome/comments/pneza1/gdbus_call_for_moving_windows_not_working_in/)
	Running global.context.unsafe_mode = true in Looking Glass re-enables the functionality, but only temporarily.
	You can play around with what's possible in GJS using Gnome's 'Looking Glass' debugger: Alt+F2, and run lg

	"""
	dbusBase = dbusBase()
	dbudGnome = dbudGnome()


	@keyword('Call dbus Method')
	def call_dbus_method(self, bus='session', busname=None, objectpath=None, interface=None, method=None, args=None):
		"""Call a dbus Method directly, this keyword provides direct access to the dbus,
			intended as a workaround when there is no keyword available
			'bus':			Which bus is the method on, valid options are system and session (default is session)
			'busname': 		Bus Name (e.g. org.gnome.Shell)
			'objectpath':	Object Path  (e.g. /org/gnome/Shell)
			'interface':	Interface Name  (e.g. org.gnome.Shell.Screenshot)
			'method':		Method Name (e.g. ScreenshotWindow)
			`args`:			Method Arguments

		"""
		try:
			proxy = self.dbusBase.bus[bus].get_object(busname, objectpath)
			strmethod = "proxy.{}(, dbus_interface='{}')".format(method, interface)
			result = eval(strmethod)
			print(result)
			return result
		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Failed to execute `{}` on {} bus {} and object path {}".format(strmethod, bus, busname, objectpath)
			raise AssertionError(emsg)

	@keyword('Call Gnome JS')
	def call_gnome_js(self, js):
		"""Call Gnome JavaScript

		"""
		try:
			eval = self.dbudGnome._gnome_gjs(js)
			print("eval:",eval)
			data = json.loads(eval[1])
			return data
		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Failed to execute `{}`".format(js)
			raise AssertionError(emsg)



	@keyword('Get Window List')
	def get_window_list(self):
		"""Get a list of open windows

		"""
		try:
			wl = {}
			wl['gnome'] = self.dbudGnome.get_window_list
			# wl['kde'] = raise AssertionError("not implimented")

			data = wl[self.dbusBase.de]()
			return data

		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Unable get window list"
			raise AssertionError(emsg)


	@keyword('Get Active Window')
	def get_active_window(self):
		"""Get Active Window, returns the currntly active window
		"""
		try:
			fn = {}
			fn['gnome'] = self.dbudGnome.get_active_window
			# fn['kde'] = raise AssertionError("not implimented")

			data = fn[self.dbusBase.de]()
			return data

		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Unable get window list"
			raise AssertionError(emsg)


	@keyword('Activate Window')
	def activate_window(self, window=None, title=None):
		"""Activate window, brings the selected window to the forground and makes it active
			`window`: 	Window object (from Get Window List)
			`title`: 	Title string
		"""
		try:
			fn = {}
			fn['gnome'] = self.dbudGnome.activate_window
			# fn['kde'] = raise AssertionError("not implimented")

			data = fn[self.dbusBase.de](window, title)
			# return data

		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Unable get window list"
			raise AssertionError(emsg)


	@keyword('Move Window')
	def move_window(self, window=None, title=None):
		"""Move window to specified location
			`window`: 	Window object (from Get Window List)
			`title`: 	Title string
		"""
		pass


	@keyword('Resize Window')
	def resize_window(self, window=None, title=None):
		"""Resize window to specified size
			`window`: 	Window object (from Get Window List)
			`title`: 	Title string
		"""
		pass


	@keyword('Minimise Window')
	def minimise_window(self, window=None, title=None):
		"""Minimise the specified window
			`window`: 	Window object (from Get Window List)
			`title`: 	Title string
		"""
		pass


	@keyword('Restore Window')
	def restore_window(self, window=None, title=None):
		"""Restore the specified window, restores the window to a normal floating window, (not Maximised and not Minimised)
			`window`: 	Window object (from Get Window List)
			`title`: 	Title string
		"""
		pass


	@keyword('Maximise Window')
	def maximise_window(self, window=None, title=None):
		"""Maximise the specified window
			`window`: 	Window object (from Get Window List)
			`title`: 	Title string
		"""
		pass


	@keyword('Close Window')
	def close_window(self, window=None, title=None):
		"""Close the specified window
			`window`: 	Window object (from Get Window List)
			`title`: 	Title string
		"""
		pass


	@keyword('Click Location')
	def click_location(self, x=None, y=None):
		"""Click Location by x,y co-ordinates
			`x`: 	x co-ordinate
			`y`: 	y co-ordinate
		"""
		pass


	@keyword('Type')
	def type_text(self, instring=None, interval=100):
		"""Type a string
			`instring`: 	The string to type
			`interval`: 	Time in miliseconds between keys (default 100)
		"""
		pass


	@keyword('Take Screenshot')
	def take_screenshot(self, include_cursor=True, flash=False, mode="Full Screen", area=[0,0,0,0], filename=None, filename_prefix="dbus_screenshot"):
		"""Take Screenshot
			`include_cursor`: 	show the mouse pointer (default true)
			`flash`: 			make the screen flash (default false)
			`mode`:				Mode options are Full Screen, Active Window, Area
			`area`:				list of 4 intergers [x, y, width, height]
			`filename`: 		override the default filename (you need to control the number progression if required, and the file path)
			`filename_prefix`: 	override the default filename prefix
		"""
		try:
			fn = {}
			fn['gnome'] = self.dbudGnome.take_screenshot
			# fn['kde'] = raise AssertionError("not implimented")

			data = fn[self.dbusBase.de](include_cursor, flash, mode, area, filename, filename_prefix)
			# return data

		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Unable get window list"
			raise AssertionError(emsg)

		# Auto It keywords for consideration:
		#
		# Auto It Set Option - Auto It specific
		# Block Input - good ides maybe future version
		# CD Tray - good ides maybe future version
		# Clip Get - good ides maybe future version
		# Clip Put - good ides maybe future version

		# Control Click - A windows control (button maybe?)
		# Control Command
		# Control Disable
		# Control Enable
		# Control Focus
		# Control Get Focus
		# Control Get Handle
		# Control Get Pos Height
		# Control Get Pos Width
		# Control Get Pos X
		# Control Get Pos Y
		# Control Get Text
		# Control Hide
		# Control List View
		# Control Move
		# Control Send
		# Control Set Text
		# Control Show
		# Control Tree View

		# Drive Map Add - network drives not sure about this
		# Drive Map Del
		# Drive Map Get

		# Get Active Window Image - done - screenshot active window

		# Get Auto It Version - Auto It specific

		# Get Screen Image - done - screenshot full screen

		# Get Version - not sure?

		# Ini Delete - ini files, easy to impliment not sure it's needed?
		# Ini Read
		# Ini Write

		# Init - Auto It specific
		# Is Admin - Windows OS specific

		# Mouse Click - We'll need all the same sorts of mouse handeling
		# Mouse Click Drag
		# Mouse Down
		# Mouse Get Cursor
		# Mouse Get Pos X
		# Mouse Get Pos Y
		# Mouse Move
		# Mouse Up
		# Mouse Wheel

		# Opt - Auto It specific

		# Pixel Checksum - these Pixel functions could be useful, but probably a candidate for a later version
		# Pixel Get Color
		# Pixel Search

		# Process Close - Process keywords use ProcessLibrary or OperatingSystemLibrary
		# Process Exists
		# Process Set Priority
		# Process Wait
		# Process Wait Close

		# Reg Delete Key - Windows OS specific, Linux doesn't have a system registry
		# Reg Delete Val
		# Reg Enum Key
		# Reg Enum Val
		# Reg Read
		# Reg Write

		# Run - Process keywords use ProcessLibrary or OperatingSystemLibrary
		# Run As Set
		# Run Wait

		# Send - need this - Sends simulated keystrokes to the active window.

		# Shutdown - Shuts down the system. - OperatingSystemLibrary?

		# Statusbar Get Text - Retrieves the text from a standard status bar control.
		# Tool Tip - Creates a tooltip anywhere on the screen.

		# Wait For Active Window - Wait up to TimeOut seconds for the window with the given WindowTitle and optional WindowText to appear. Force this to be the active window after it appears.  Optionally do a full screen capture on failure.
		# Win Activate - Activates (gives focus to) a window.
		# Win Active - Checks to see if a specified window exists and is currently active.
		# Win Close - Closes a window.
		# Win Exists - Checks to see if a specified window exists.
		# Win Get Caret Pos X - Returns the coordinates of the caret in the foreground window.
		# Win Get Caret Pos Y - Returns the coordinates of the caret in the foreground window.
		# Win Get Class List - Retrieves the classes from a window.
		# Win Get Client Size Height - Retrieves the size of a given window's client area.
		# Win Get Client Size Width - Retrieves the size of a given window's client area.
		# Win Get Handle - Retrieves the internal handle of a window.
		# Win Get Pos Height - Retrieves the position and size of a given window.
		# Win Get Pos Width - Retrieves the position and size of a given window.
		# Win Get Pos X - Retrieves the position and size of a given window.
		# Win Get Pos Y - Retrieves the position and size of a given window.
		# Win Get Process - Retrieves the Process ID (PID) associated with a window.
		# Win Get State - Retrieves the state of a given window.
		# Win Get Text - Retrieves the text from a window.
		# Win Get Title - Retrieves the full title from a window.
		# Win Kill - Forces a window to close.
		# Win List - Retrieves a list of windows.
		# Win Menu Select Item - Invokes a menu item of a window.
		# Win Minimize All - Minimizes all windows.
		# Win Minimize All Undo - Undoes a previous WinMinimizeAll function.
		# Win Move - Moves and/or resizes a window.
		# Win Set On Top - Change a window's "Always On Top" attribute.
		# Win Set State - Shows, hides, minimizes, maximizes, or restores a window.
		# Win Set Title - Changes the title of a window.
		# Win Set Trans - Sets the transparency of a window.
		# Win Wait - Pauses execution of the script until the requested window exists.
		# Win Wait Active - Pauses execution of the script until the requested window is active.
		# Win Wait Close -Pauses execution of the script until the requested window does not exist.
		# Win Wait Not Active - Pauses execution of the script until the requested window is not active.
		#












#

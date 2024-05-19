
from robot.api.deco import keyword, library


@library
class dbusLibrary:
	"""robotframework-dbus

	A Robot Framework library to help automation of linux desktop applications
	"""

	system_bus = None
	session_bus = None
	screenshot_count = 0

	def __init__(self):
		self.system_bus = dbus.SystemBus()
		self.session_bus = dbus.SessionBus()

	@keyword('Get Window List')
	def get_window_list(self):
		"""Get a list of open windows

		"""

		try:
			gshell = session_bus.get_object('org.gnome.Shell', '/org/gnome/Shell')
			eval = gshell.Eval("global.get_window_actors().map(a=>a.meta_window).map(w=>({class: w.get_wm_class(), class_instance: w.get_wm_class_instance(), pid: w.get_pid(), id: w.get_id(), maximized: w.get_maximized(), focus: w.has_focus(), title: w.get_title()}))", dbus_interface='org.gnome.Shell')
			print("eval:",eval)

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
		pass


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
			`filename`: 		override the default filename (you need to control the number progression if required)
			`filename_prefix`: 	override the default filename prefix
		"""

		# Take Screenshot
		# Info from d-feet:
		# Method Name:		Screenshot (Boolean include_cursor, Boolean flash, String filename) ↦ (Boolean success, String filename_used)
		# Bus name:			org.gnome.Shell
		# Object Path:		/org/gnome/Shell/Screenshot
		# Interface:		org.gnome.Shell.Screenshot

		try:
			if filename is None:
				self.screenshot_count = self.screenshot_count + 1
				filename = "{}_{}".format(filename_prefix, self.screenshot_count)
				print("filename:",filename)

			gshellscrsht = session_bus.get_object('org.gnome.Shell', '/org/gnome/Shell/Screenshot')
			if mode == "Full Screen":
				scrsht = gshellscrsht.Screenshot(include_cursor, flash, filename, dbus_interface='org.gnome.Shell.Screenshot')
			elif mode == "Active Window":
				scrsht = gshellscrsht.ScreenshotWindow(include_cursor, flash, filename, dbus_interface='org.gnome.Shell.Screenshot')
			elif mode == "Area":
				scrsht = gshellscrsht.ScreenshotArea(area[0], area[1], area[2], area[3], flash, filename, dbus_interface='org.gnome.Shell.Screenshot')
			else:
				emsg = "Invalid Mode: '{}', valid modes are Full Screen, Active Window or Area".format(mode)
				raise AssertionError(emsg)

			print("scrsht:",scrsht)
			print("<img src='./{}'>".format(filename))
		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Failed to take screenshot"
			raise AssertionError(emsg)














#

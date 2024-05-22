
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















#

import dbus
import json
import os
import platform
import requests

from robot.api.deco import keyword, library


@library
class dbusLibrary:
	"""robotframework-dbus

	A Robot Framework library to help automation of linux desktop applications
	"""
	bus = {}
	screenshot_count = 0
	de = None

	def __init__(self):
		self._checkos()
		self._checkde()

		if 'system' not in self.bus:
			self.bus['system'] = dbus.SystemBus()
		if 'session' not in self.bus:
			self.bus['session'] = dbus.SessionBus()

		if self.de == 'gnome':
			self._gnome_prereqs()

	def _checkos(self):
		sys = platform.system()
		if sys != "Linux":
			emsg = "{} is not supported by dbusLibrary".format(sys)
			raise AssertionError(emsg)

	def _checkde(self):
		xcd = os.environ.get('XDG_CURRENT_DESKTOP').split(':')
		self.de = xcd[1].lower()
		# self.de = os.environ.get('DESKTOP_SESSION')
		if self.de not in ['gnome', 'kde']:
			emsg = "{} is not yet supported by dbusLibrary".format(self.de)
			raise AssertionError(emsg)

	def _gnome_prereqs(self):
		# Install window calls extended (https://github.com/hseliger/window-calls-extended)
		# To manually install, copy extension.js and metadata.json into a folder by
		# 	(exactly!! Gnome will not load the extension if the folder name does not match the uuid from the metadata)
		# 	name of window-calls-extended@hseliger.eu under your ~/.local/share/gnome-shell/extensions folder.

		# >>> os.path.expanduser("~/.local/share/gnome-shell/extensions")
		# '/home/dave/.local/share/gnome-shell/extensions'
		# extentionspath = os.path.expanduser("~/.local/share/gnome-shell/extensions")
		#
		# wcepath = os.path.join(extentionspath, "window-calls-extended@hseliger.eu")
		#
		# if not os.path.exists(wcepath):
		# 	os.makedirs(wcepath)
		#
		# # https://raw.githubusercontent.com/hseliger/window-calls-extended/main/extension.js
		# baseurl = "https://raw.githubusercontent.com/hseliger/window-calls-extended/main/"
		# # extension.js
		# jsfile = os.path.join(wcepath, "extension.js")
		# self._download_file(baseurl + "extension.js", jsfile)
		# # metadata.json
		# jsonfile = os.path.join(wcepath, "metadata.json")
		# self._download_file(baseurl + "metadata.json", jsonfile)
		pass

	def _gnome_gjs(self, js):
		gshell = self.bus['session'].get_object('org.gnome.Shell', '/org/gnome/Shell')
		eval = gshell.Eval(js, dbus_interface='org.gnome.Shell')
		return eval

	def _download_file(self, fromurl=None, tofile=None):

		# url = "http://download.thinkbroadband.com/10MB.zip"
		response = requests.get(fromurl, stream=True)

		with open(tofile, "wb") as handle:
			for data in tqdm(response.iter_content()):
				handle.write(data)


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
			proxy = self.bus[bus].get_object(busname, objectpath)
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


	@keyword('Get Window List')
	def get_window_list(self):
		"""Get a list of open windows

		"""
		try:
			if self.de == 'gnome':
				# gshell = self.bus['session'].get_object('org.gnome.Shell', '/org/gnome/Shell')
				# eval = gshell.Eval("global.get_window_actors().map(a=>a.meta_window).map(w=>({class: w.get_wm_class(), class_instance: w.get_wm_class_instance(), pid: w.get_pid(), id: w.get_id(), maximized: w.get_maximized(), focus: w.has_focus(), title: w.get_title()}))", dbus_interface='org.gnome.Shell')
				# print("eval:",eval)
				# https://discourse.gnome.org/t/how-to-get-get-windows-width-height-x-coordinate-y-coordinate-activeworkspace-and-isviewable/10881

				# eval = self._gnome_gjs("""global.get_window_actors()
				# 								.map(a=>a.meta_window)
				# 								.map(w=>({
				# 									class: w.get_wm_class(),
				# 									class_instance: w.get_wm_class_instance(),
				# 									id: w.get_id(),
				# 									width: w.get_width(),
				# 									height: w.get_height(),
				# 									x: w.get_x(),
				# 									y: w.get_y(),
				# 									maximized: w.get_maximized(),
				# 									focus: w.has_focus(),
				# 									title: w.get_title()}))""")
				# eval = self._gnome_gjs("""global.get_window_actors()
				# 								.map(a=>a.meta_window)
				# 								.map(w=>({
				# 									class: w.get_wm_class(),
				# 									class_instance: w.get_wm_class_instance(),
				# 									id: w.get_id(),
				# 									maximized: w.get_maximized(),
				# 									focus: w.has_focus(),
				# 									title: w.get_title(),
				# 									w: w
				# 									}))""")
				# eval = self._gnome_gjs("""global.get_window_actors()
				# 								.map(a=>({
				# 									class: a.meta_window.get_wm_class(),
				# 									class_instance: a.meta_window.get_wm_class_instance(),
				# 									id: a.meta_window.get_id(),
				# 									width: a.get_width(),
				# 									height: a.get_height(),
				# 									x: a.get_x(),
				# 									y: a.get_y(),
				# 									maximized: a.meta_window.get_maximized(),
				# 									focus: a.meta_window.has_focus(),
				# 									title: a.meta_window.get_title(),
				# 									w: a.meta_window,
				# 									a: a
				# 									}))""")
				eval = self._gnome_gjs("""global.get_window_actors()
												.map(a=>({
													class: a.meta_window.get_wm_class(),
													class_instance: a.meta_window.get_wm_class_instance(),
													id: a.meta_window.get_id(),
													width: a.get_width(),
													height: a.get_height(),
													x: a.get_x(),
													y: a.get_y(),
													maximized: a.meta_window.get_maximized(),
													focus: a.meta_window.has_focus(),
													title: a.meta_window.get_title(),
													}))""")
				# print("eval:",eval)
				data = json.loads(eval[1])
				return data

			if self.de == 'kde':
				raise AssertionError("not implimented")

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

			if self.de == 'gnome':
				gshellscrsht = self.bus['session'].get_object('org.gnome.Shell', '/org/gnome/Shell/Screenshot')
				if mode == "Full Screen":
					scrsht = gshellscrsht.Screenshot(include_cursor, flash, filename, dbus_interface='org.gnome.Shell.Screenshot')
				elif mode == "Active Window":
					scrsht = gshellscrsht.ScreenshotWindow(include_cursor, flash, filename, dbus_interface='org.gnome.Shell.Screenshot')
				elif mode == "Area":
					scrsht = gshellscrsht.ScreenshotArea(area[0], area[1], area[2], area[3], flash, filename, dbus_interface='org.gnome.Shell.Screenshot')
				else:
					emsg = "Invalid Mode: '{}', valid modes are Full Screen, Active Window or Area".format(mode)
					raise AssertionError(emsg)

			if self.de == 'kde':
				raise AssertionError("not implimented")

			print("scrsht:",scrsht)
			print("<img src='./{}'>".format(filename))
		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Failed to take screenshot"
			raise AssertionError(emsg)














#

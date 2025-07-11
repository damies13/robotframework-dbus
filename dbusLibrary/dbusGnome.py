import dbus
import json
import os

from robot.api import logger


from .dbusBase import dbusBase
# from .osio import osio


class dbusGnome:
	"""
	https://unix.stackexchange.com/questions/399753/how-to-get-a-list-of-active-windows-when-using-wayland
	Sadly, this no longer works on Gnome 41 for security reasons (https://www.reddit.com/r/gnome/comments/pneza1/gdbus_call_for_moving_windows_not_working_in/)
	Running global.context.unsafe_mode = true in Looking Glass re-enables the functionality, but only temporarily.
	You can play around with what's possible in GJS using Gnome's 'Looking Glass' debugger: Alt+F2, and run lg

	- https://askubuntu.com/questions/1412130/dbus-calls-to-gnome-shell-dont-work-under-ubuntu-22-04

	"""
	screenshot_count = 0
	dbusBase = dbusBase()
	# osio = osio()
	unsafe_mode = False

	def __init__(self):
		shellver = self._get_gnome_version()
		if float(shellver) >= 41.0 and not self.unsafe_mode:
			self._enable_gnome_unsafe_mode()

	def _enable_gnome_unsafe_mode(self):
		logger.info("Need Gnome unsafe_mode")
		logger.console("Need Gnome unsafe_mode")
		# self._gnome_gjs("global.context.unsafe_mode = true")

		# open 'Looking Glass' debugger: Alt+F2, and run lg
		# self.osio.press_combination("alt", "f2")

		# input "global.context.unsafe_mode = true"

		# self.unsafe_mode = True

		# self.osio.press_combination("esc")

		# logger.console("Enabled Gnome unsafe_mode")


	def _get_gnome_version(self):
		# need to get Gnome version
		#
		# Bus name:			org.gnome.Shell
		# Object Path:		/org/gnome/Shell
		# Interface:		org.gnome.Shell
		# Properties: 		ShellVersion
		try:
			gshell = self.dbusBase.bus['session'].get_object('org.gnome.Shell', '/org/gnome/Shell')
			# gshell = self.dbusBase.bus['session'].get('org.gnome.Shell', '/org/gnome/Shell')
			# print(gshell)
			# eval = gshell.ShellVersion(dbus_interface='org.gnome.Shell')
			# iface = self.dbusBase.bus['system'].Interface(dev, 'org.gnome.Shell')
			# props = iface.GetAllProperties()
			# logger.info("props: {}".format(props))

			properties_manager = dbus.Interface(gshell, 'org.freedesktop.DBus.Properties')
			eval = properties_manager.Get('org.gnome.Shell', 'ShellVersion')

			# eval = gshell.ShellVersion

			# print(eval)
			# logger.info("Gnome ShellVersion: {}".format(eval))
			# logger.console("Gnome ShellVersion: {}".format(eval))
			return eval
		except AssertionError as e:
			print(e)
			logger.console("AssertionError: {}".format(e))
			raise AssertionError(e)
		except Exception as e:
			print(e)
			logger.console("Exception: {}".format(e))
			raise AssertionError(e)



	def _gnome_gjs(self, js):
		try:
			print(js)
			gshell = self.dbusBase.bus['session'].get_object('org.gnome.Shell', '/org/gnome/Shell')
			print(gshell)
			eval = gshell.Eval(js, dbus_interface='org.gnome.Shell')
			print(eval)
			return eval
		except AssertionError as e:
			print(e)
			raise AssertionError(e)
		except Exception as e:
			print(e)
			raise AssertionError(e)

	def get_window_list(self):
		"""Get a list of open windows

		"""
		try:
			# gshell = self.dbusBase.bus['session'].get_object('org.gnome.Shell', '/org/gnome/Shell')
			# eval = gshell.Eval("global.get_window_actors().map(a=>a.meta_window).map(w=>({class: w.get_wm_class(), class_instance: w.get_wm_class_instance(), pid: w.get_pid(), id: w.get_id(), maximized: w.get_maximized(), focus: w.has_focus(), title: w.get_title()}))", dbus_interface='org.gnome.Shell')
			# print("eval:",eval)
			# https://discourse.gnome.org/t/how-to-get-get-windows-width-height-x-coordinate-y-coordinate-activeworkspace-and-isviewable/10881

			# eval = self.dbusGnome._gnome_gjs("""global.get_window_actors()
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
			# eval = self.dbusGnome._gnome_gjs("""global.get_window_actors()
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
			# eval = self.dbusGnome._gnome_gjs("""global.get_window_actors()
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
												pid: a.meta_window.get_pid(),
												width: a.get_width(),
												height: a.get_height(),
												x: a.get_x(),
												y: a.get_y(),
												maximized: a.meta_window.get_maximized(),
												focus: a.meta_window.has_focus(),
												title: a.meta_window.get_title(),
												}))""")
			print("eval:",eval)
			data = json.loads(eval[1])
			return data

		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Unable get window list"
			raise AssertionError(emsg)

	def get_active_window(self):
		"""Get Active Window, returns the currntly active window
		"""

		eval = self._gnome_gjs("""
			function isfocused(window){
				if (window.focus == true)
				{
					return true;
				}
			}

			global.get_window_actors()
				.map(a=>({
					class: a.meta_window.get_wm_class(),
					class_instance: a.meta_window.get_wm_class_instance(),
					id: a.meta_window.get_id(),
					pid: a.meta_window.get_pid(),
					width: a.get_width(),
					height: a.get_height(),
					x: a.get_x(),
					y: a.get_y(),
					maximized: a.meta_window.get_maximized(),
					focus: a.meta_window.has_focus(),
					title: a.meta_window.get_title(),
					})).filter(isfocused)
			""")
		# print("eval:",eval)
		data = json.loads(eval[1])
		return data[0]


	def activate_window(self, window=None, title=None):
		"""Activate window, brings the selected window to the forground and makes it active
			`window`: 	Window object (from Get Window List)
			`title`: 	Title string
		"""
		# jsarr = []
		# if window is not None:
		# 	if 'id' in window:
		# 		jsarr.append("function winfilter(window){")
		# 		jsarr.append("	if (window.id == {})".format(window['id']))
		# 		jsarr.append("	{")
		# 		jsarr.append("		return true;")
		# 		jsarr.append("	}")
		# 		jsarr.append("}")
		# if title is not None:
		# 	jsarr.append("function winfilter(window){")
		# 	jsarr.append("	if (window.title == '{}')".format(title))
		# 	jsarr.append("	{")
		# 	jsarr.append("		return true;")
		# 	jsarr.append("	}")
		# 	jsarr.append("}")
		#
		#
		# jsarr.append("")
		# jsarr.append("let w = global.get_window_actors()")
		# jsarr.append(" 	.map(a=>({")
		# # jsarr.append(" 		class: a.meta_window.get_wm_class(),")
		# # jsarr.append(" 		class_instance: a.meta_window.get_wm_class_instance(),")
		# jsarr.append(" 		id: a.meta_window.get_id(),")
		# # jsarr.append(" 		pid: a.meta_window.get_pid(),")
		# # jsarr.append(" 		width: a.get_width(),")
		# # jsarr.append(" 		height: a.get_height(),")
		# # jsarr.append(" 		x: a.get_x(),")
		# # jsarr.append(" 		y: a.get_y(),")
		# # jsarr.append(" 		maximized: a.meta_window.get_maximized(),")
		# # jsarr.append(" 		focus: a.meta_window.has_focus(),")
		# jsarr.append(" 		title: a.meta_window.get_title(),")
		# jsarr.append(" 		})).filter(winfilter)")
		#
		# jsarr.append("")
		# jsarr.append("w[0].activate(0)")


	    # let win = global.get_window_actors().find(w => w.meta_window.get_id() == winid);
	    # return win;
		jsarr = []
		if window is not None:
			if 'id' in window:
				jsarr.append("let win = global.get_window_actors().find(w => w.meta_window.get_id() == {});".format(window['id']))
		if title is not None:
			jsarr.append("let win = global.get_window_actors().find(w => w.meta_window.get_title() == '{}');".format(title))

		jsarr.append("")
		jsarr.append("win.meta_window.activate(0)")



		jsstr = "\n".join(jsarr)
		eval = self._gnome_gjs(jsstr)
		print("eval:",eval)
		# data = json.loads(eval[1])
		# return data[0]


	def take_screenshot(self, include_cursor=True, flash=False, mode="Full Screen", area=[0,0,0,0], filename=None, filename_prefix="dbusGnome_screenshot"):
		"""Take Screenshot
			`include_cursor`: 	show the mouse pointer (default true)
			`flash`: 			make the screen flash (default false)
			`mode`:				Mode options are Full Screen, Active Window, Area
			`area`:				list of 4 intergers [x, y, width, height]
			`filename`: 		override the default filename (you need to control the number progression if required, and the file path)
			`filename_prefix`: 	override the default filename prefix
		"""
		# Take Screenshot
		# Info from d-feet:
		# Method Name:		Screenshot (Boolean include_cursor, Boolean flash, String filename) ↦ (Boolean success, String filename_used)
		# Bus name:			org.gnome.Shell
		# Object Path:		/org/gnome/Shell/Screenshot
		# Interface:		org.gnome.Shell.Screenshot
		try:
			filepath = filename
			if filename is None:
				self.screenshot_count = self.screenshot_count + 1
				filename = "{}_{}.png".format(filename_prefix, self.screenshot_count)
				print("filename:",filename)
				logger.info("filename: %s" % filename)

				filepath = os.path.join(os.getcwd(), filename)
				# print("filepath:",filepath)
				logger.info("filepath: %s" % filepath)

			gshellscrsht = self.dbusBase.bus['session'].get_object('org.gnome.Shell', '/org/gnome/Shell/Screenshot')
			if mode == "Full Screen":
				scrsht = gshellscrsht.Screenshot(include_cursor, flash, filepath, dbus_interface='org.gnome.Shell.Screenshot')
			elif mode == "Active Window":
				include_frame = True
				scrsht = gshellscrsht.ScreenshotWindow(include_frame, include_cursor, flash, filepath, dbus_interface='org.gnome.Shell.Screenshot')
			elif mode == "Area":
				scrsht = gshellscrsht.ScreenshotArea(area[0], area[1], area[2], area[3], flash, filepath, dbus_interface='org.gnome.Shell.Screenshot')
			else:
				emsg = "Invalid Mode: '{}', valid modes are Full Screen, Active Window or Area".format(mode)
				raise AssertionError(emsg)


			# print("scrsht:",scrsht)
			# print(r'<img src="./{}">'.format(filename))
			logger.info('<img src="./{}" style="width: 99%;">'.format(filename), html=True)
		except AssertionError as e:
			raise AssertionError(e)
		except Exception as e:
			print(e)
			emsg = "Failed to take screenshot"
			raise AssertionError(emsg)




		# function checkid(word){
		#   if (word.focus == true)
		#   {
		#     return true;
		#   }
		# }
		#
		#
		# const words = [{'class': 'Gnome-terminal', 'class_instance': 'gnome-terminal-server', 'id': 516822647, 'pid': 39896, 'width': 966, 'height': 1001, 'x': 502, 'y': 160, 'maximized': 0, 'focus': false, 'title': 'dave@hp-elite-desk-800-g3: ~'}, {'class': 'Org.gnome.Nautilus', 'class_instance': 'org.gnome.Nautilus', 'id': 516822648, 'pid': 102083, 'width': 1434, 'height': 1281, 'x': 2564, 'y': 67, 'maximized': 0, 'focus': false, 'title': 'BCE'}, {'class': 'Org.gnome.Nautilus', 'class_instance': 'org.gnome.Nautilus', 'id': 516824209, 'pid': 102083, 'width': 1434, 'height': 1281, 'x': 2534, 'y': 35, 'maximized': 0, 'focus': false, 'title': 'Monash University'}, {'class': 'teams-for-linux', 'class_instance': 'teams-for-linux', 'id': 516821698, 'pid': 4027, 'width': 1928, 'height': 1166, 'x': 2550, 'y': 263, 'maximized': 0, 'focus': false, 'title': 'Chat | Brad Cunningham, Dinesh Kumar | Microsoft Teams'}, {'class': 'Microsoft-edge', 'class_instance': 'crx__faolnafnngnfdaknnbpnkhgohbobgegn', 'id': 516826442, 'pid': 499710, 'width': 1450, 'height': 1402, 'x': 3644, 'y': 6, 'maximized': 0, 'focus': false, 'title': 'Outlook (PWA) - Email - David Amies - Outlook'}, {'class': 'Google-chrome', 'class_instance': 'google-chrome', 'id': 516826805, 'pid': 511992, 'width': 2241, 'height': 1369, 'x': 245, 'y': 37, 'maximized': 0, 'focus': false, 'title': 'CITROEN C4 HEATER/ AC CONTROLS, DIGITAL CLIMATE TYPE 03/05-09/11 | eBay - Google Chrome'}, {'class': 'Gnome-terminal', 'class_instance': 'gnome-terminal-server', 'id': 516824217, 'pid': 39896, 'width': 1065, 'height': 1186, 'x': 2552, 'y': 244, 'maximized': 0, 'focus': false, 'title': 'dave@hp-elite-desk-800-g3: ~/Documents/Github/tritusa/BCE/Data'}, {'class': 'Org.gnome.Nautilus', 'class_instance': 'org.gnome.Nautilus', 'id': 516826003, 'pid': 102083, 'width': 1434, 'height': 1281, 'x': 2644, 'y': 41, 'maximized': 0, 'focus': false, 'title': 'BCE'}, {'class': 'Org.gnome.Nautilus', 'class_instance': 'org.gnome.Nautilus', 'id': 516824218, 'pid': 102083, 'width': 1434, 'height': 1281, 'x': 119, 'y': 90, 'maximized': 0, 'focus': false, 'title': 'Screenshots'}, {'class': 'Pulsar', 'class_instance': 'pulsar', 'id': 516827977, 'pid': 689491, 'width': 1741, 'height': 1279, 'x': 3388, 'y': 80, 'maximized': 0, 'focus': false, 'title': 'Project — ~/Documents/Github/tritusa — Pulsar'}, {'class': 'Gjs', 'class_instance': 'gjs', 'id': 516828063, 'pid': 703178, 'width': 2560, 'height': 1440, 'x': 2560, 'y': 0, 'maximized': 0, 'focus': false, 'title': '@!2560,0;BDHF'}, {'class': 'Gjs', 'class_instance': 'gjs', 'id': 516828064, 'pid': 703178, 'width': 2560, 'height': 1440, 'x': 0, 'y': 0, 'maximized': 0, 'focus': false, 'title': '@!0,0;BDHF'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516822394, 'pid': 72823, 'width': 1617, 'height': 1459, 'x': 31, 'y': 10, 'maximized': 0, 'focus': false, 'title': 'pve0 - Proxmox Virtual Environment — Mozilla Firefox'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516822391, 'pid': 72823, 'width': 1564, 'height': 1440, 'x': 994, 'y': 4, 'maximized': 0, 'focus': false, 'title': '5 m Proa kostenloser Bauplan — Mozilla Firefox'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516822461, 'pid': 72823, 'width': 1385, 'height': 1459, 'x': 1162, 'y': 4, 'maximized': 0, 'focus': false, 'title': 'OC Requests Log — Mozilla Firefox'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516823886, 'pid': 72823, 'width': 1385, 'height': 1459, 'x': 3287, 'y': -23, 'maximized': 0, 'focus': false, 'title': 'RobotFramework - RIDE dashboard in Crowdin — Mozilla Firefox'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516823871, 'pid': 72823, 'width': 1647, 'height': 1456, 'x': 584, 'y': 4, 'maximized': 0, 'focus': false, 'title': 'Create a Voice Recorder using Python - GeeksforGeeks — Mozilla Firefox'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516827129, 'pid': 72823, 'width': 1385, 'height': 1459, 'x': 2965, 'y': -23, 'maximized': 0, 'focus': false, 'title': 'wroclaw galerie - Google Search — Mozilla Firefox'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516822396, 'pid': 72823, 'width': 1647, 'height': 1456, 'x': 58, 'y': 4, 'maximized': 0, 'focus': false, 'title': 'Notifications — Mozilla Firefox'}, {'class': 'Pulsar', 'class_instance': 'pulsar', 'id': 516827974, 'pid': 689491, 'width': 1741, 'height': 1279, 'x': 547, 'y': 171, 'maximized': 0, 'focus': false, 'title': 'untitled — ~/Documents/tmp — Pulsar'}, {'class': 'Pulsar', 'class_instance': 'pulsar', 'id': 516827975, 'pid': 689491, 'width': 1741, 'height': 1329, 'x': 772, 'y': 121, 'maximized': 0, 'focus': false, 'title': 'setup-agent.py — ~/Documents/Github/rfswarm — Pulsar'}, {'class': 'Pulsar', 'class_instance': 'pulsar', 'id': 516827976, 'pid': 689491, 'width': 1741, 'height': 1279, 'x': 643, 'y': 163, 'maximized': 0, 'focus': false, 'title': 'Project — ~/Documents/Github/pyDesktopAccessibility — Pulsar'}, {'class': 'Slack', 'class_instance': 'slack', 'id': 516821695, 'pid': 3382, 'width': 1505, 'height': 1309, 'x': 3625, 'y': 30, 'maximized': 0, 'focus': false, 'title': '* robocon (Channel) - RobotFramework - Slack'}, {'class': 'Pulsar', 'class_instance': 'pulsar', 'id': 516827973, 'pid': 689491, 'width': 1741, 'height': 1329, 'x': 75, 'y': 121, 'maximized': 0, 'focus': false, 'title': 'Project — ~/Documents/Github/TestDataTable — Pulsar'}, {'class': 'Org.gnome.Nautilus', 'class_instance': 'org.gnome.Nautilus', 'id': 516822521, 'pid': 102083, 'width': 1434, 'height': 1281, 'x': 166, 'y': 102, 'maximized': 0, 'focus': false, 'title': 'extensions'}, {'class': 'Brave-browser', 'class_instance': 'brave-browser', 'id': 516828013, 'pid': 694609, 'width': 1666, 'height': 1432, 'x': 3416, 'y': 1, 'maximized': 0, 'focus': false, 'title': 'Inbox (21,443) - damies13@gmail.com - Gmail - Brave'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516822395, 'pid': 72823, 'width': 1385, 'height': 1459, 'x': 2601, 'y': -23, 'maximized': 0, 'focus': false, 'title': 'Robot Framework User Guide — Mozilla Firefox'}, {'class': 'GitFiend', 'class_instance': 'gitfiend', 'id': 516824251, 'pid': 262852, 'width': 1627, 'height': 1133, 'x': 242, 'y': 245, 'maximized': 0, 'focus': false, 'title': 'GitFiend - /home/dave/Documents/Github/robotframework-dbus'}, {'class': 'Brave-browser', 'class_instance': 'crx_agimnkijcaahngcdmfeangaknmldooml', 'id': 516828014, 'pid': 694609, 'width': 1787, 'height': 1390, 'x': 2570, 'y': 27, 'maximized': 0, 'focus': false, 'title': 'YouTube - Sunset update on Trimaran Twillight - YouTube'}, {'class': 'discord', 'class_instance': 'discord', 'id': 516821696, 'pid': 3437, 'width': 1425, 'height': 1320, 'x': 3701, 'y': 130, 'maximized': 0, 'focus': false, 'title': 'namies, Sen, nari, Spam - Discord'}, {'class': 'D-feet', 'class_instance': 'd-feet', 'id': 516828065, 'pid': 703348, 'width': 2293, 'height': 1162, 'x': 81, 'y': 60, 'maximized': 0, 'focus': false, 'title': 'd-feet'}, {'class': 'D-feet', 'class_instance': 'd-feet', 'id': 516828089, 'pid': 703348, 'width': 452, 'height': 455, 'x': 350, 'y': 351, 'maximized': 0, 'focus': false, 'title': 'Execute D-Bus Method'}, {'class': 'firefox', 'class_instance': 'Navigator', 'id': 516822397, 'pid': 72823, 'width': 1647, 'height': 1456, 'x': 859, 'y': 4, 'maximized': 0, 'focus': false, 'title': 'How to Tile Windows - Desktop - GNOME Discourse — Mozilla Firefox'}, {'class': 'Pulsar', 'class_instance': 'pulsar', 'id': 516827972, 'pid': 689491, 'width': 1741, 'height': 1279, 'x': 716, 'y': 129, 'maximized': 0, 'focus': false, 'title': 'dbustests.robot — ~/Documents/Github/robotframework-dbus — Pulsar'}, {'class': 'Gnome-terminal', 'class_instance': 'gnome-terminal-server', 'id': 516822146, 'pid': 39896, 'width': 1371, 'height': 1204, 'x': 1191, 'y': 74, 'maximized': 0, 'focus': true, 'title': 'dave@hp-elite-desk-800-g3: ~/Documents/Github/robotframework-dbus/Tests'}, {'class': 'Gnome-shell', 'class_instance': 'gnome-shell', 'id': 516821683, 'pid': 1937, 'width': 1, 'height': 1, 'x': -200, 'y': -200, 'maximized': 0, 'focus': false, 'title': 'gnome-shell'}, {'class': 'firefox', 'class_instance': 'firefox', 'id': 516822463, 'pid': 72823, 'width': 1, 'height': 1, 'x': -99, 'y': -99, 'maximized': 0, 'focus': false, 'title': 'Firefox'}, {'class': 'Org.gnome.Nautilus', 'class_instance': 'org.gnome.Nautilus', 'id': 516822524, 'pid': 102083, 'width': 1, 'height': 1, 'x': -99, 'y': -99, 'maximized': 0, 'focus': false, 'title': 'org.gnome.Nautilus'}, {'class': 'Org.gnome.Nautilus', 'class_instance': 'org.gnome.Nautilus', 'id': 516822526, 'pid': 102083, 'width': 1, 'height': 1, 'x': -99, 'y': -99, 'maximized': 0, 'focus': false, 'title': 'org.gnome.Nautilus'}, {'class': 'Gnome-terminal', 'class_instance': 'gnome-terminal-server', 'id': 516822650, 'pid': 39896, 'width': 1, 'height': 1, 'x': -99, 'y': -99, 'maximized': 0, 'focus': false, 'title': 'Terminal'}];
		# const result = words.filter(checkid);
		#
		# console.log(result);


#

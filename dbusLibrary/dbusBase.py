import dbus
import os
import platform
import requests


class dbusBase:

	bus = {}
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

	# def de(self):
	# 	return 	self.de

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

	def download_file(self, fromurl=None, tofile=None):

		# url = "http://download.thinkbroadband.com/10MB.zip"
		response = requests.get(fromurl, stream=True)

		with open(tofile, "wb") as handle:
			for data in tqdm(response.iter_content()):
				handle.write(data)

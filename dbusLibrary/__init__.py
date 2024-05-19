
from robot.api.deco import keyword, library


@library
class dbusLibrary:
	"""robotframework-dbus

	A Robot Framework library to help automation of linux desktop applications
	"""

	system_bus = None
	session_bus = None

	def __init__(self):
		self.system_bus = dbus.SystemBus()
		self.session_bus = dbus.SessionBus()

	@keyword('Get Window List')
	def get_counter(self, counterpath=None, hostname="localhost"):
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












#

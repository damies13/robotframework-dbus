
import dbus


# gdbus call   --session   --dest org.gnome.Shell   --object-path /org/gnome/Shell   --method org.gnome.Shell.Eval
# "global.get_window_actors().map(a=>a.meta_window).map(w=>({class: w.get_wm_class(), title: w.get_title()}))"
# | sed -E -e "s/^\(\S+, '//" -e "s/'\)$//"


system_bus = dbus.SystemBus()
session_bus = dbus.SessionBus()

print(session_bus.list_names())

gshell = session_bus.get_object('org.gnome.Shell', '/org/gnome/Shell')


# var = gshell.getProperties(dbus_interface='org.gnome.Shell')
# print("var:",var)


# eval = gshell.Eval("global.get_window_actors().map(a=>a.meta_window).map(w=>({class: w.get_wm_class(), title: w.get_title()}))")
# eval = gshell.Eval("global.get_window_actors().map(a=>a.meta_window).map(w=>({class: w.get_wm_class(), title: w.get_title()}))", dbus_interface='org.gnome.Shell')

eval = gshell.Eval("global.get_window_actors().map(a=>a.meta_window).map(w=>({class: w.get_wm_class(), class_instance: w.get_wm_class_instance(), pid: w.get_pid(), id: w.get_id(), maximized: w.get_maximized(), focus: w.has_focus(), title: w.get_title()}))", dbus_interface='org.gnome.Shell')
print("eval:",eval)

# {"class":"Brave-browser","class_instance":"crx_agimnkijcaahngcdmfeangaknmldooml","pid":12207,"id":516821994,"maximized":0,"focus":false,"title":"YouTube - SpaceX Starship Flight 4: Has the FAA REALLY Just Cleared the Way!? - YouTube"},
# gshell.FocusApp("516821994", dbus_interface='org.gnome.Shell')




# Take Screenshot
# Info from d-feet:
# Method Name:		Screenshot (Boolean include_cursor, Boolean flash, String filename) ↦ (Boolean success, String filename_used)
# Bus name:			org.gnome.Shell
# Object Path:		/org/gnome/Shell/Screenshot
# Interface:		org.gnome.Shell.Screenshot

# gshellscrsht = session_bus.get_object('org.gnome.Shell', '/org/gnome/Shell/Screenshot')
# scrsht = gshellscrsht.Screenshot(True, True, "", dbus_interface='org.gnome.Shell.Screenshot')
# print("scrsht:",scrsht)


#

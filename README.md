# robotframework-dbus
A library of Robot Framework keywords that use dbus to control Linux desktop apps


A road block for now, keyboard and mouse control:
- first I reviewed how this is done in ImageHorizon Library, it's done with pyAutoGUI, the problem with this is it only works on X11, but not on Wayland
- next I searched for how to trigger keyboard and mouse activity in Wayland, all I found was ydotool (a wayland compatable clone of sorts of xdotool), I also found ydotool can be used with python via pyydotool, but it's very difficult to setup ydotool, and the version of ydotool that's packaged in most distro's is v0.8.12 but pyydotool needs ydotool version 1.0.1 or higher, so we would need to commpile ydotool to go with pyydotool. then there is a some tricky configuration needed to make the ydotoold service run before you can use pyydotool.
- I also looked for a way to do keyboard and mouse control via dbus or GJS/Kwin but no luck so far

Need to keep exploring for possible solutions.


## Gnome 41+

    Gnome 41+ and higher needs Gnome unsafe_mode Enabled 

    To enable Gnome unsafe_mode:

	- open 'Looking Glass' debugger: 
      - press Alt+F2
      - type "lg"
      - press enter
	- type "global.context.unsafe_mode = true" into Looking Glass
	- press ESC to close Looking Glass


*** Settings ***
Library 	../dbusLibrary/

*** Test Cases ***
Window List
	${wlist}= 	Get Window List
	Log 	${wlist}


Get Currently Active Window
	${window}= 	Get Active Window
	Log 	${window}

Activate A Window
	# Call Gnome JS 	this._get_window_by_wid("516828014").meta_window.activate()
	# Call Gnome JS 	let win = this._get_window_by_wid(516828014).meta_window;
	# ...							win.activate(0);
	# Call Gnome JS 	global._get_window_by_wid("516828014").meta_window.activate(0)

	${wlist}= 	Get Window List
	Log 	${wlist}
	FOR		${w} 	IN 	@{wlist}
			IF 	"YouTube" in "${w}[title]"
				Activate Window 	${w}
			END
	END

	# Sleep    1
	#
	# FOR		${w} 	IN 	@{wlist}
	# 		IF 	"Pulsar" in "${w}[title]"
	# 			Log		${w}[title]
	# 			Log		${w}
	# 			Activate Window 	title=${w}[title]
	# 			Sleep    1
	# 		END
	# END


Take Screenshots

	Take Screenshot
	Take Screenshot 	mode=Active Window

	Take Screenshot 	mode=Area 		area=[0,0,200,100]


Type Some Things

	${wlist}= 	Get Window List
	Log 	${wlist}
	FOR		${w} 	IN 	@{wlist}
			IF 	"Untitled Document" in "${w}[title]"
				Activate Window 	${w}
			END
	END

	Type 		Something
	Press Key Combination 	shift 	a
	Press Key Combination 	shift 	b
	Press Key Combination 	shift 	c

	Press Key Combination 	control 	s
	Press Key Combination 	escape
	

#

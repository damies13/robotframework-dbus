*** Settings ***
Library 	../dbusLibrary/

*** Test Cases ***
Window List
	${wlist}= 	Get Window List
	Log 	${wlist}




#

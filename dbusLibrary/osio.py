import pyautogui

from robot.api import logger

class osio:

	# ag = pyautogui()

	def press_combination(self, *keys):
		listkeys = list(keys)
		logger.info("keys: {}".format(listkeys))
		pyautogui.press(listkeys)

	def type(self, text):
		logger.info("text: {}".format(text))
		pyautogui.typewrite(text)











#

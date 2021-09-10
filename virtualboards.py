#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# virtualboards.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# Configures multiple boards to be run in a separate thread.
#
# ## #############################################################

import sys
from atexit import register
from threading import Thread
from board import LedsBoard, TemperatureBoard
from tkinter import Tk, mainloop
import RPi.GPIO as GPIO

_board = None
_board_type = None
_async_board_thread = None


def exit_handler():
	global _board
	print('Shutting down board GUI')
	# try:
	# 	_board.close()
	# 	_board = None
	# except:
	# 	pass
	if _async_board_thread:
		_async_board_thread.join()
	sys.exit(0)
# end def



def _async_board_worker():
	global _async_board_thread
	global _board

	if _board_type == 'leds':
		_board = LedsBoard()
		_board.connect(GPIO._io_pins)
	elif _board_type == 'temp':
		_board = TemperatureBoard()
	elif _board_type == 'dimm':
		return
	elif _board_type == 'ctrl':
		return
	else:
		return

	try:
		mainloop()
	except:
		pass
	_async_board_thread = None
# end def



def _setup():
	global _async_board_thread
	_async_board_thread = Thread(target=_async_board_worker)
	_async_board_thread.daemon = True
	register(exit_handler)
# end def



def _check_board():
	if (_board is not None) or (_async_board_thread is not None):
		raise RuntimeError("A board is already running")
# end def



def run_led_board():
	_check_board()
	_setup()

	global _board_type
	_board_type = "leds"
	_async_board_thread.start()
# end def



def run_temperature_board():
	_check_board()
	_setup()

	global _board_type
	_board_type = "temp"
	_async_board_thread.start()
# end def



def run_dimmer_board():
	_check_board()
	_setup()

	global _board_type
	_async_board_thread.start()
# end def



def run_tempcontrol_board():
	_check_board()
	_setup()

	global _board_type

	_async_board_thread.start()
# end def



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# board.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# ## #############################################################

from .tboard import TemperatureBoard
from .tcboard import TempCtrlBoard
from tkinter import mainloop

def main():
	# board = TempCtrlBoard()
	board = TemperatureBoard()
	mainloop()

if __name__ == '__main__':
	main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# board.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################

from .tcboard import TempCtrlBoard
from tkinter import mainloop

def main():
	board = TempCtrlBoard()
	mainloop()

if __name__ == '__main__':
	main()

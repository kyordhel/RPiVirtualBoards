#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# led.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

from .__common import _img

class LED:
	def __init__(self):
		self._on = False
		self._bg = PhotoImage(file=_img('led-background.png'))
		self._fg = PhotoImage(file=_img('led-foreground.png'))
		self._im = PhotoImage(file=_img('led-bright.png'))
	# end def


	def on(self):
		self._on = True
	# end def

	def off(self):
		self._on = False
	# end def

	def draw(self, canvas, xpos, ypos):
		canvas.create_image(xpos, ypos, anchor=NW, image=self._bg)
		if self._on:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._im)
		canvas.create_image(xpos, ypos, anchor=NW, image=self._fg)
	# end def
#end class

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# sevenseg.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################

from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

from .__common import _img

class SevenSeg:
	def __init__(self):
		self._bgi = PhotoImage(file=_img('7s-background.png'))
		self._fgi = PhotoImage(file=_img('7s-foreground.png'))
		self._sai = PhotoImage(file=_img('7s-a.png'))
		self._sbi = PhotoImage(file=_img('7s-b.png'))
		self._sci = PhotoImage(file=_img('7s-c.png'))
		self._sdi = PhotoImage(file=_img('7s-d.png'))
		self._sei = PhotoImage(file=_img('7s-e.png'))
		self._sfi = PhotoImage(file=_img('7s-f.png'))
		self._sgi = PhotoImage(file=_img('7s-g.png'))
		self._dpi = PhotoImage(file=_img('7s-dp.png'))
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.e = 0
		self.f = 0
		self.g = 0
		self.dp = 0
	# end def

	def draw(self, canvas, xpos, ypos):
		canvas.create_image(xpos, ypos, anchor=NW, image=self._bgi)
		if self.a:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sai)
		if self.b:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sbi)
		if self.c:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sci)
		if self.d:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sdi)
		if self.e:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sei)
		if self.f:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sfi)
		if self.g:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._sgi)
		if self.dp:
			canvas.create_image(xpos, ypos, anchor=NW, image=self._dpi)
		canvas.create_image(xpos, ypos, anchor=NW, image=self._fgi)
	# end def

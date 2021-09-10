#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# tcboard.py
#
# Author:  Mauricio Matamoros
# Licence: MIT
# Date:    2020.03.01
#
# ## #############################################################

import re
import sys
import time
import random
import struct
from os import path, _exit
from threading import Thread, Timer, Lock
from tkinter import *

from PIL import Image, ImageTk, ImageEnhance

from .led import LED
from .sevenseg import SevenSeg
from .bcd7seg import BCD7Seg
from smbus2 import Vi2cSlave

class TemperatureBoard(Vi2cSlave):
	def __init__(self):
		super().__init__(10)
		self._templock = Lock()
		self._temp = 0
		self._data = None

		# GUI
		random.seed(time.time())
		self.gui = Tk(className=" Temperature Sensor Board")
		self.gui.bind("<<UpdateData>>", self._update_data_sent)
		self._io_pins = {}
		self.controls = {}
		for i in range(1, 28):
			self._io_pins[i] = None
		self._initialize_components()
		self._setup_timer()
		self.running = True
	# end def

	def __del__(self):
		_exit(1)
	# end def

	def _initialize_components(self):
		# set window size
		self.gui.geometry("250x120")
		#set window color
		self.gui.configure(bg="#000000")
		self.gui.protocol("WM_DELETE_WINDOW", self._on_closing)

		# Control instantiation
		self.strTempR = StringVar(self.gui)
		self.strTempS = StringVar(self.gui)
		self.strDataS = StringVar(self.gui)
		self.strSFreq = StringVar(self.gui)

		# Validators
		validatetemp = self.gui.register(self._validatetemp)
		validatefreq = self.gui.register(self._validatefreq)

		self.lblTempR = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="Temperature (real):")
		self.txtTempR = Entry(self.gui, justify="right",
			width=10, textvariable=self.strTempR,
			validate='all', validatecommand=(validatetemp, '%P'))

		self.lblTempS = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="Temperature (sensor):")
		self.txtTempS = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strTempS)

		self.lblSFreq = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="ADC Frequency:")
		self.txtSFreq = Entry(self.gui, justify="right",
			width=10, textvariable=self.strSFreq,
			validate='all', validatecommand=(validatefreq, '%P'))

		self.lblDataS = Label(self.gui, anchor="w",
			bg="#000000", fg="#e0e0e0",
			text="Data sent:")
		self.txtDataS = Entry(self.gui, justify="right",
			width=10, state="readonly", textvariable=self.strDataS)


		# Control initialization
		self.lblTempR.grid(row=0, column=0, sticky="w", padx=2, pady=2)
		self.txtTempR.grid(row=0, column=1, sticky="w", padx=2, pady=2)
		self.lblSFreq.grid(row=1, column=0, sticky="w", padx=2, pady=2)
		self.txtSFreq.grid(row=1, column=1, sticky="w", padx=2, pady=2)
		self.lblTempS.grid(row=2, column=0, sticky="w", padx=2, pady=2)
		self.txtTempS.grid(row=2, column=1, sticky="w", padx=2, pady=2)
		self.lblDataS.grid(row=3, column=0, sticky="w", padx=2, pady=2)
		self.txtDataS.grid(row=3, column=1, sticky="w", padx=2, pady=2)


		self.strTempR.set("22.0")
		self.strTempS.set("0.0")
		self.strSFreq.set("3")
		# Create canvas
		# self.canvas = Canvas(self.gui, width=510, height=270, bg='#296e01', bd=0, highlightthickness=0, relief='ridge')
		# self.canvas.pack()
		# self._draw_canvas()
		# self.canvas.after(1, self._redraw)
	# end def

	def _draw_canvas(self):
		self.canvas.delete(ALL)
		# Add 7-segments to canvas
		# self.sevenSeg.draw(self.canvas, 197, 90)
		# Add LEDs to canvas
		# xpos = 20
		# ypos = 20
		# for led in self.leds:
		# 	led.draw(self.canvas, xpos, ypos)
		# 	xpos += 60
		self.canvas.update()
	# end def

	def _redraw(self):
		self._update_status()
		self._draw_canvas()
		if self.running:
			self.canvas.after(20, self._redraw)
	# end def

	def _on_closing(self):
		self.running = False
		self.timer.cancel()
		self.timer = None
		self.disconnect()
		self.gui.destroy()
		self.gui.quit()
		sys.exit()
	# end def

	def _update_status(self):
		pass
	# end def


	def _validatetemp(self, value):
		try:
			temp = float(value)
			if temp >= 0 and temp <= 150:
				return True
			return False
		except:
			return False

	def _validatefreq(self, value):
		try:
			freq = int(value)
			if freq > 0 and freq <= 100:
				return True
			return False
		except:
			return False

	def _setup_timer(self):
		try:
			delay = 1 / float(self.strSFreq.get())
		except:
			delay = 0.1
		self.timer = Timer(delay, self._timer_task)
		self.timer.daemon = True
		self.timer.start()

	def _timer_task(self):
		try:
			temp = float(self.strTempR.get())
		except:
			pass

		temp += 0.01 * random.randint(-50, 50)
		self._templock.acquire()
		self._temp = temp
		self._templock.release()

		try:
			self.strTempS.set("{:.2f}".format(temp))
		except:
			pass

		if self.running:
			self._setup_timer()
	# end def

	def _update_data_sent(self, event):
		sdata = "0x" + "".join("{:02x}".format(x) for x in self._data)
		self.strDataS.set(sdata)

	def close(self):
		self._on_closing()

	def read(self):
		"""Reads a byte stream from the slave"""
		self._templock.acquire()
		self._data = struct.pack("<f", self._temp)
		self._templock.release()

		try:
			self.gui.event_generate("<<UpdateData>>", when="tail")
		except:
			pass
		return self._data
	#end def

	def write(self, value):
		"""Writes byte stream to the slave"""
		# Sets the ADC frequency (capped to 100Hz)
		freq = struct.unpack('<f', value)
		if freq > 100:
			freq = 100
		elif freq < 1:
			freq = 1
		freq = int(freq)
		self.strSFreq.set(freq)

	#end def


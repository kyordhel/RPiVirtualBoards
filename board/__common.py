#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# __common.py
#
# Author: Mauricio Matamoros
# Licence: MIT
# Date:
#
# ## #############################################################


from os import path

_img_path = "img"
_img_path = path.join(path.dirname(path.realpath(__file__)), _img_path)

def _img(file_name):
	return path.join(_img_path, file_name)

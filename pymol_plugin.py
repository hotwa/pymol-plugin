#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file        :pymol_plugin.py
@Description:       :
@Date     :2021/09/04 17:36:10
@Author      :hotwa
@version      :1.0
'''
from pymol import cmd
from pymol_dependence import autoshow

cmd.extend('autoshow', autoshow)
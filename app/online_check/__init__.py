#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 13:51:58 2018

@author: akurm
"""

from flask import Blueprint
bp = Blueprint('online_check', __name__)

from app.online_check import routes, attachments



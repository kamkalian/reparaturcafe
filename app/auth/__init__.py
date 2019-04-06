#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 13:51:58 2018

@author: akurm
"""

from flask import Blueprint
bp = Blueprint('auth', __name__)

from app.auth import routes



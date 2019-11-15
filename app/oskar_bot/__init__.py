#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, current_app
bp = Blueprint('oskar_bot', __name__)

from app.oskar_bot import bot



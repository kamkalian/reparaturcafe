#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 08:26:34 2018

@author: akurm
"""

from flask import render_template, url_for, redirect, request, flash, jsonify
from app.online_check.forms import CreateRequestForm
from app.online_check import bp
from app.models import Category

@bp.route('/create_request', methods=['GET', 'POST'])
def create_request():
    form = CreateRequestForm()

    categories = Category.query.all()
    categories.insert(0, Category(name='Bitte auswaehlen...', samples=''))
    form.set_categories(categories)
    # print(categories[0].name)

    if form.validate_on_submit():

        return redirect(url_for('main.index'))

    return render_template('online_check/create_request.html', title='Online Check', form=form)


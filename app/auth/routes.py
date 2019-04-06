#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 08:26:34 2018

@author: akurm
"""

from flask import render_template, url_for, redirect, request, flash, jsonify
from app import db
from app.auth import bp
from app.models import User
from flask_login import current_user, login_user, logout_user
from app.models import User, Role
from app.auth.forms import LoginForm, RegistrationForm, UserEditForm
from werkzeug.urls import url_parse
from flask_login import login_required
import json


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('auth/user.html', title=username, user=user)


@bp.route('/user_edit/<username>', methods=['GET', 'POST'])
@login_required
def user_edit(username):
    form = UserEditForm()

    if not current_user.username == username:
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        user.username = form.username.data
        user.email = form.email.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        db.session.commit()
        flash('saved', 'success')
        return redirect(url_for('auth.user', username=user.username))
    form.email.default = current_user.email
    form.username.default = current_user.username
    form.lastname.default = current_user.lastname
    form.firstname.default = current_user.firstname
    form.process()
    return render_template('auth/user_edit.html', title=username, form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role == 'admin':
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('New User registered.', 'success')
            return redirect(url_for('auth.login'))
        return render_template('auth/register.html', title='Register', form=form)
    else:
        return redirect(url_for('main.index'))


@bp.route('/user_management', methods=['GET', 'POST'])
@login_required
def user_management():
    if current_user.role == 'admin':
        user_list = User.query.all()
        roles = Role.query.all()
        return render_template('auth/user_management.html', title='User Management', user_list=user_list, roles=roles)
    else:
        return redirect(url_for('main.index'))

@bp.route('/change_user_role', methods=['POST'])
def change_user_role():
    info_state = 'danger'
    info_msg = 'error'

    user_id = json.loads(request.form['user_id'])
    new_role = request.form['new_role']

    user = User.query.filter_by(id=user_id).first()
    user.role = new_role

    db.session.commit()
    info_msg = 'saved'
    info_state = 'success'

    return jsonify({'info_msg': info_msg, 'info_state': info_state})

#! /usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint
from flask import render_template
from flask import request
from flask import g
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from app.forms import SignUpForm
from app.forms import LoginForm
from app.database import User
from app.database import Task
from app.utils import make_salt_passwd
from app.utils import make_passwd_hash
from app.utils import format_form_errors

mod = Blueprint('index', __name__)

@mod.route('/')
def index():
  return render_template('index.html')

@mod.route('/sign_up', methods = ['POST', 'GET'])
def sign_up():
  errors = []
  form = SignUpForm(request.form)
  if request.method == 'POST' and form.validate():
    username = form.username.data
    real_name = form.real_name.data
    salt, passwd_hash = make_salt_passwd(form.password.data)
    user = list(User.view('users/by_username', key = username))
    if user:
      errors.append('User already exists')
    else:
      new_user = User(username = username, real_name = real_name,
        salt = salt, password = passwd_hash)
      g.db.save_doc(new_user)
      flash('You have successfully registered')
      return redirect(url_for('index.index'))
  errors.extend(format_form_errors(form.errors.items()))
  return render_template('sign_up.html', form = form, errors = errors)

@mod.route('/login', methods = ['POST', 'GET'])
def login():
  errors = []
  form = LoginForm(request.form)
  if request.method == 'POST' and form.validate():
    username = form.username.data
    password = form.password.data
    users = list(User.view('users/by_username', key = username))
    if not users:
      errors.append('Wrong username')
    else:
      user = users[0]
      if make_passwd_hash(user.salt, password) != user.password:
        errors.append('Wrong password')
      else:
        session['logged_in'] = True
        session['uid'] = user._id
        session['username'] = user.username
        flash('You were logged in')
        return redirect(url_for('index.index'))
  errors.extend(format_form_errors(form.errors.items()))
  return render_template('login.html', form = form, errors = errors)

@mod.route('/logout')
def logout():
  session.pop('logged_in', None)
  session.pop('uid', None)
  session.pop('username', None)

  flash('You were logged out')
  return redirect(url_for('index.index'))

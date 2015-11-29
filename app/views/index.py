#! /usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint
from flask import render_template
from flask import request
from app.forms import SignUpForm

mod = Blueprint('index', __name__)

@mod.route('/')
def index():
  return 'It works!'

@mod.route('/sign_up', methods = ['POST', 'GET'])
def sign_up():
  form = SignUpForm(request.form)
  if request.method == 'POST' and form.validate():
    pass
  return render_template('sign_up.html', form = form)

@mod.route('/login')
def login():
  return 'Login'

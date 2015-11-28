#! /usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint

mod = Blueprint('index', __name__)

@mod.route('/')
def index():
  return 'It works!'

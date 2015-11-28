#! /usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint

mod = Blueprint('users', __name__, url_prefix = '/users')

#! /usr/bin/env python
# -*- coding: utf-8 -*

from flask import Blueprint

mod = Blueprint('tasks', __name__, url_prefix = '/tasks')

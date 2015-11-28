#! /usr/bin/env python
# -*- coding: utf-8 -*

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app.views import index
from app.views import users
from app.views import tasks

app.register_blueprint(index.mod)
app.register_blueprint(users.mod)
app.register_blueprint(tasks.mod)

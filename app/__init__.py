#! /usr/bin/env python
# -*- coding: utf-8 -*

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app.views import index
from app.views import users
from app.views import tasks
from app.views import projects

from flask import g
from database import User
from database import Task
from database import Comment
from database import Project
from database import connect_db

app.register_blueprint(index.mod)
app.register_blueprint(users.mod)
app.register_blueprint(tasks.mod)
app.register_blueprint(projects.mod)

@app.before_request
def before_request():
  g.db = connect_db(app.config['DB'])
  User.set_db(g.db)
  Task.set_db(g.db)
  Comment.set_db(g.db)
  Project.set_db(g.db)

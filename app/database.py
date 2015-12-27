#! /usr/bin/env python
# -*- coding: utf-8 -*

from couchdbkit import loaders
from couchdbkit import Server
from couchdbkit import Document
from couchdbkit import StringProperty
from couchdbkit import SetProperty
from couchdbkit import DateProperty
from couchdbkit import DateTimeProperty

def connect_db(db_name):
  srv = Server()
  return srv.get_or_create_db(db_name)

def init_db(db_name):
  db = connect_db(db_name)
  loader = loaders.FileSystemDocsLoader('app/_design')
  loader.sync(db, verbose = True)

class User(Document):
  username = StringProperty()
  real_name = StringProperty()
  salt = StringProperty()
  password = StringProperty()
  email = StringProperty()

class Project(Document):
  author = StringProperty()
  title = StringProperty()
  start_date = DateProperty()
  due_date = DateProperty()
  text = StringProperty()

class Task(Document):
  author = StringProperty()
  assigned = StringProperty()
  priority = StringProperty()
  title = StringProperty()
  text = StringProperty()
  tags = StringProperty()
  status = StringProperty()
  project = StringProperty()
  comments = SetProperty()
  create_date = DateTimeProperty()
  update_date = DateTimeProperty()
  due_date = DateProperty()

class Comment(Document):
  author = StringProperty()
  text = StringProperty()
  date = DateTimeProperty()
  task_id = StringProperty()

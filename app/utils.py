#! /usr/bin/env python
# -*- coding: utf-8 -*

import uuid
import hashlib
import functools

from flask import abort
from flask import session

from app.database import Task
from app.forms import EditTaskForm

def login_required(f):
  @functools.wraps(f)
  def wrapped(*args, **kwargs):
    if not session.get('logged_in'):
      abort(401)
    return f(*args, **kwargs)
  return wrapped

def format_form_errors(raw_errors):
  out = []
  for field, errors in raw_errors:
    for error in errors:
      print (field, error)
      print field
      print error
      error_msg = 'Error in field: %s - %s' % (field, error)
      out.append(error_msg)
  return out

def make_passwd_hash(salt, password):
  return hashlib.md5(salt + password).hexdigest()

def make_salt_passwd(passwd):
  salt = uuid.uuid4().hex
  password = make_passwd_hash(salt, passwd)
  return salt, password

def update_task(task, form):
  assigned = form.assigned.data
  priority = form.priority.data
  title = form.title.data
  text = form.text.data
  tags = set(form.tags.data.split())
  status = form.status.data
  project = form.project.data
  return task

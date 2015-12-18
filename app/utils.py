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
      error_msg = 'Error in field: %s - %s' % (field, error)
      out.append(error_msg)
  return out

def make_passwd_hash(salt, password):
  return hashlib.md5(salt + password).hexdigest()

def make_salt_passwd(passwd):
  salt = uuid.uuid4().hex
  password = make_passwd_hash(salt, passwd)
  return salt, password

def update_form(task, form):
  form.assigned.data = task.assigned
  form.priority.data = task.priority
  form.title.data = task.title
  form.text.data = task.text
  form.tags.data = ' '.join(task.tags)
  form.status.data = task.status
  form.project.data = task.project
  form.due_date.data = task.due_date
  return form

def update_task(task, form):
  task.assigned = form.assigned.data
  task.priority = form.priority.data
  task.title = form.title.data
  task.text = form.text.data
  task.tags = set(form.tags.data.split())
  task.status = form.status.data
  task.project = form.project.data
  task.due_date = form.due_date.data
  return task

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
from flask import abort
from app import app
from app.database import User
from app.database import Task
from app.database import Comment
from app.utils import format_form_errors
from app.utils import login_required
from app.forms import EditTaskForm
from app.forms import CommentForm
from werkzeug import secure_filename
import datetime
import os
import random

NEW_TASK_ID = u'new'
UPLOADED_FILES = os.path.join(app.root_path, app.config.get('UPLOAD_FOLDER'))
mod = Blueprint('tasks', __name__, url_prefix = '/tasks')

@mod.route('/edit/<id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
  errors = []
  form = EditTaskForm(request.form)
  task = None

  possible_assigned = [elem.username for elem in list(User.view('users/by_username'))]
 
  if id == NEW_TASK_ID:
    task = Task()
  else:
    if not g.db.doc_exist(id):
      abort(404)
    task = Task.get(id)
    if request.method == 'GET':
      form = EditTaskForm(obj=task)
  
  form.assigned.choices = zip(possible_assigned, possible_assigned)
  form.assigned.default = 0
  form.project.choices = [('test', 'test')]
  form.project.default = 0

  if request.method == 'POST' and form.validate():
    form.populate_obj(task)
    task.author = session['username']
    task.update_date = datetime.datetime.utcnow()
    task.tags = ' '.join(set(task.tags.split()))
    
    if id == NEW_TASK_ID:
      task.create_date = task.update_date

    if id != NEW_TASK_ID:
      for ff in request.files.keys():
        f = request.files[ff]
        if f:
          fname = secure_filename(f.filename)
          fld = os.path.join(UPLOADED_FILES, id)
          if not os.path.exists(fld):
            os.mkdir(fld)
          target_path = os.path.join(fld, fname)
          while os.path.exists(target_path):
            filename, ext = os.path.splitext(target_path)
            r = ''.join(random.choice('0123456789abcdef') for i in range(8))
            target_path = os.path.join(fld, filename + '-' + r + ext)
          f.save(target_path)
          flash('Successfully uploaded %s' % fname)
    task.save()
    flash('Task was successfully %s' % ('created' if id == NEW_TASK_ID else 'updated'))
    return redirect(url_for('index.index'))

  errors.extend(format_form_errors(form.errors.items()))
  return render_template('task_edit.html', id = id, form = form, errors = errors)

@mod.route('/<id>', methods = ['GET', 'POST'])
@login_required
def show(id):
  if not g.db.doc_exist(id):
    abort(404)

  errors = []
  task = Task.get(id)
  form = CommentForm(request.form)
  comments = list(Comment.view('comments/by_task_id', key = id))
  comments = sorted(comments, key = lambda x: x.date)

  if request.method == 'POST' and form.validate():
    new_comment = Comment()
    new_comment.author = session['username']
    new_comment.text = form.text.data
    new_comment.date = datetime.datetime.utcnow()
    new_comment.task_id = id
    new_comment.save()
    flash('Comment was successfully added')
    return redirect(url_for('tasks.show', id = id))

  fpath = os.path.join(UPLOADED_FILES, id)
  files = None
  if os.path.exists(fpath):
    files = os.listdir(fpath)

  errors.extend(format_form_errors(form.errors.items()))
  return render_template('task_show.html', \
    task = task, comments = comments, form = form, errors = errors, \
    files = files)

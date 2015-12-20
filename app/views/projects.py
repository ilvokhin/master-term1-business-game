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
from app.database import Project
from app.utils import format_form_errors
from app.utils import login_required
from app.forms import EditTaskForm
from app.forms import EditProjectForm
from app.forms import CommentForm
from werkzeug import secure_filename
import datetime
import os
import random

NEW_PROJECT_ID = u'new'
UPLOADED_FILES = os.path.join(app.root_path, app.config.get('UPLOAD_FOLDER'))
mod = Blueprint('projects', __name__, url_prefix = '/projects')

@mod.route('/edit/<id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
  errors = []
  form = EditProjectForm(request.form)
  project = None

  if id == NEW_PROJECT_ID:
    project = Project()
  else:
    if not g.db.doc_exist(id):
      abort(404)
    project = Project.get(id)
    if request.method == 'GET':
      form = EditProjectForm(obj=project)
      pass

  if request.method == 'POST' and form.validate():
    form.populate_obj(project)
    project.author = session['username']

    '''
    if id != NEW_PROJECT_ID:
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
    '''
    project.save()
    flash('Project was successfully %s' % ('created' if id == NEW_PROJECT_ID else 'updated'))
    return redirect(url_for('index.index'))

  errors.extend(format_form_errors(form.errors.items()))
  return render_template('project_edit.html', id = id, form = form, errors = errors)

@mod.route('/<id>', methods = ['GET', 'POST'])
@login_required
def show(id):
  if not g.db.doc_exist(id):
    abort(404)

  errors = []
  project = Project.get(id)

  '''
  fpath = os.path.join(UPLOADED_FILES, id)
  files = None
  if os.path.exists(fpath):
    files = os.listdir(fpath)
  '''

  return render_template('project_show.html', \
    project = project, errors = errors)

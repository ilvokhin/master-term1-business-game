#! /usr/bin/env python
# -*- coding: utf-8 -*

from wtforms import Form
from wtforms import TextField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import TextAreaField
from wtforms import validators

class SignUpForm(Form):
  username = TextField('username', [validators.Length(min=4, max=50)])
  real_name = TextField('real name', [validators.Length(min=6)])
  password = PasswordField \
  (
    'password',
    [
      validators.Required(),
      validators.EqualTo('confirm', message = 'Passwords must match.')
    ]
  )
  confirm = PasswordField('confirm password')

class LoginForm(Form):
  username = TextField('username', [validators.Required()])
  password = PasswordField('password', [validators.Required()])

class EditTaskForm(Form):
  assigned = SelectField('assigned')

  priority_choices = []
  for elem in ['hight', 'normal', 'low']:
    priority_choices.append((elem, elem))
  priority = SelectField('priority', choices = priority_choices)

  title = TextField('title', [validators.Length(min=6)])
  text = TextAreaField('text')
  tags = TextField('tags')

  status_choices = []
  for elem in ['new', 'work', 'ready', 'close']:
    status_choices.append((elem, elem))
  status = SelectField('status', choices = status_choices)

  project = SelectField('project')

class CommentForm(Form):
  text = TextAreaField('text', [validators.Length(min=2)])

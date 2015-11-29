#! /usr/bin/env python
# -*- coding: utf-8 -*

import uuid
import hashlib

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

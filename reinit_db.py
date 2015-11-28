#! /usr/bin/env python
# -*- coding: utf-8 -*

from app import app
from app.database import init_db

init_db(app.config.get('DB'))

#! /usr/bin/env python
# -*- coding: utf-8 -*

import datetime
from app import app
from app.database import User
from app.database import Task
from app.database import Comment
from app.database import Project
from app.database import connect_db
from app.utils import make_salt_passwd

DEFAULT_PASSWORD = 'password'
USERS = [
  {'username' : 'a.sukharev', 'name' : u'Сухарев Андрей'},
  {'username' : 'a.frolov', 'name' : u'Александр Фролов'},
  {'username' : 'i.cheglakov', 'name' : u'Иван Чеглаков'},
  {'username' : 'm.chistyakov', 'name' : u'Максим Чистяков'},
  {'username' : 'a.kritsky', 'name' : u'Артем Крицкий'}
]

PROJECTS = [
  {'author' : 'a.sukharev', 'title' : u'Системный анализ краудфаундинговых платформ', \
    'descr' : u'Мы смотрим в будущее, ощущая настоящее.'}
]

TASKS = [
  #
  {'author' : 'a.sukharev', 'assigned' : 'a.frolov', 'priority' : 'Normal', \
    'title' : u'Анализ платформы кикстартер', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'a.frolov', 'priority' : 'Normal', \
    'title' : u'Сравнение с платформами indiegogo и GoFundMe', \
    'text' : u'Нужно сравнить две эти платформы и вставить результаты в презентацию.',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'a.frolov', 'priority' : 'High', \
    'title' : u'Проверка достоверности информации на официальных сайтах', \
    'text' : u'Так же сравнение этой информации с данными из СМИ. Срочно!',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'a.frolov', 'priority' : 'Normal', \
    'title' : u'Составлении презентации на основе информации прошедшей проверку', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  #
  {'author' : 'a.sukharev', 'assigned' : 'm.chistyakov', 'priority' : 'Normal', \
    'title' : u'Определение райтинга зарубежных СМИ', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'm.chistyakov', 'priority' : 'Normal', \
    'title' : u'Поиск статей о краудфаундинге в наиболее достоверных источниках', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'm.chistyakov', 'priority' : 'Low', \
    'title' : u'Перевод статей', \
    'text' : u'Пока общий таск, подумай, что в нем делать.',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'm.chistyakov', 'priority' : 'Normal', \
    'title' : u'Написание и адаптация собственного англоязычного материала', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  #
  {'author' : 'a.sukharev', 'assigned' : 'i.cheglakov', 'priority' : 'Normal', \
    'title' : u'Подборка и анализ наиболее успешных проектов', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'i.cheglakov', 'priority' : 'Normal', \
    'title' : u'Подборка и анализ наиболее скандальных и неудачных проектов', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'i.cheglakov', 'priority' : 'Normal', \
    'title' : u'Поиск и анализ статей в СМИ по скандальным проектам', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'i.cheglakov', 'priority' : 'Normal', \
    'title' : u'Написание статьи о формуле успеха на краудфаундинговых платформах', \
    'text' : u'Нужно объединить всю собранную информацию в нечто законченное.',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  #
  {'author' : 'a.sukharev', 'assigned' : 'a.kritsky', 'priority' : 'Normal', \
    'title' : u'Первичный анализ активов и угроз для МИС "Цифромед"', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'a.kritsky', 'priority' : 'Normal', \
    'title' : u'Составление диаграммы Coras с применением противодействия', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'a.kritsky', 'priority' : 'Normal', \
    'title' : u'Составление матрицы недопустимых рисков', \
    'text' : u'Subj',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  },
  {'author' : 'a.sukharev', 'assigned' : 'a.kritsky', 'priority' : 'High', \
    'title' : u'Составление рекомендаций по проведению аудита', \
    'text' : u'Нужно объединить всю собранную информацию информацию в нечто законченное.',
    'project' : u'Системный анализ краудфаундинговых платформ', \
    'status' : 'Done'
  }
]

def add_user(user):
  db = connect_db(app.config.get('DB'))
  User.set_db(db)
  Comment.set_db(db)
  #
  db_user = User()
  db_user.username = user['username']
  db_user.real_name = user['name']
  db_user.salt, db_user.password = make_salt_passwd(DEFAULT_PASSWORD)
  #
  db.save_doc(db_user)

def add_project(project):
  db = connect_db(app.config.get('DB'))
  Project.set_db(db)
  #
  db_project = Project()
  db_project.author = project['author']
  db_project.title = project['title']
  db_project.start_date = datetime.date.today()
  db_project.due_date = datetime.date.today()
  db_project.text = project['descr']
  #
  db.save_doc(db_project)

def add_task(task):
  db = connect_db(app.config.get('DB'))
  Task.set_db(db)
  Project.set_db(db)
  #
  db_task = Task()
  #
  db_project = list(Project.view('projects/by_title', key = task['project']))[0]
  
  db_task.author = task['author']
  db_task.assigned = task['assigned']
  db_task.priority = task['priority']
  db_task.title = task['title']
  db_task.text = task['text']
  db_task.status = task['status']
  db_task.project = db_project.title
  db_task.create_date = datetime.datetime.utcnow()
  db_task.update_date = datetime.datetime.utcnow()
  db_task.due_date = datetime.date.today()
  #
  db.save_doc(db_task)

def main():
  for user in USERS:
    add_user(user)

  for project in PROJECTS:
    add_project(project)

  for task in TASKS:
    add_task(task)

  print 'OK'

if __name__ == "__main__":
  main()

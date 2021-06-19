"""
reference: https://flask.palletsprojects.com/en/2.0.x/config/
           https://www.youtube.com/watch?v=GW_2O9CrnSU
"""

from collections import deque
from threading import Lock

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SECRET_KEY = 'thisisdemo'

    # 스케쥴러
    SCHEDULER_API_ENABLED = True

    # argocd 이벤트 큐
    ARGOCD_EVENT_QUEUE = deque()
    ARGOCD_EVENT_LOCK = Lock()

class Dev(Config):
    DEBUG = True

class Test(Config):
    TESTING = True

class Prod(Config):
    pass
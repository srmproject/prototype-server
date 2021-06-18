# -*- coding: utf-8 -*-
from flask import Flask
from apis import api_v1
from login.loginmanager import login_manager
from db.db import db
from flask_migrate import Migrate
from scheduler.create import scheduler
import logging

def create_app(mode='Dev'):
    app = Flask(__name__)

    # 설정 불러오기    
    app.config.from_object(f"flaskconfig.{mode}")
    
    # 설정 출력
    # print(app.config)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['TESTING'] = False

    # bludeprint 초기화
    app.register_blueprint(api_v1)

    # 데이터베이스 초기화
    db.init_app(app)
    migrate = Migrate(app, db)

    # Loginmanager 초기화
    login_manager.init_app(app)

    # 스케쥴러 초기화
    scheduler.init_app(app)
    logging.getLogger("apscheduler").setLevel(logging.INFO)
    from scheduler import tasks
    scheduler.start()

    return app
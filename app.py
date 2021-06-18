# -*- coding: utf-8 -*-
from flask import Flask
from apis import api_v1
from login.loginmanager import login_manager
from db.db import db
from flask_migrate import Migrate
import os

def create_app():
    app = Flask(__name__)

    # 설정 불러오기
    mode = os.environ.get('mode', 'Dev')
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

    return app
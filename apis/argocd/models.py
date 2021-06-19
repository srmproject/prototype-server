# -*- coding: utf-8 -*-
from db.db import db

class ArgoUserApps(db.Model):
    '''
        서비스 입장에서는 프로트이지만 Gialb group을 관리
    '''
    __tablename__  = 'argo_user_apps'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(300), nullable=False)
    app_name = db.Column(db.String(300), nullable=False)

    def __init__(self, project_name, app_name):
        self.project_name = project_name
        self.app_name = app_name

# -*- coding: utf-8 -*-

from config.argocd_config import get_argocdToken, get_argocdURI, get_argocdadmin
import requests
from logger.log import log
import json
from .models import ArgoUserApps
from db.db import db
import requests
class ArgocdCreateProject:
    '''
        argocd 폴더 생성
            프로젝트가 생성 될 때
    '''

    def __init__(self, project_name):
        self.project_name = project_name
        self.argocd_accesstoken = get_argocdToken()
        self.host = get_argocdURI()
        self.admin = get_argocdadmin()
    
    def create(self):
        response = False

        try:
            data = {
                "project": {
                    "metadata": { 
                        "name": f"{self.project_name}" 
                    },
                    "spec": {
                        "destinations": [
                            {
                            "server": "https://kubernetes.default.svc",
                            "namespace": f"{self.project_name}"
                            }
                        ],
                        "clusterResourceWhitelist": [
                            {
                                "group": "*",
                                "kind": "*"
                            }
                        ],
                        "sourceRepos": ["*"]
                    }
                }
            }
            request_url = """{}api/v1/projects""".format(self.host)
            headers = {"Authorization": "Bearer {}".format(self.argocd_accesstoken)}
            api_response = requests.post(request_url, data=json.dumps(data), headers=headers)

            if api_response.ok:
                response = True
                log.debug("argocd project 생성 성공")
            else:
                log.error("[324] create argocd project is failed: {}".format(api_response.json()))

        except Exception as e:
            log.error("[323] create argocd project: {}".format(e))
        finally:
            return response

class ArgocdDeploy:
    """
        argocd로 앱 배포
    """

    def __init__(self, project_name, app_name):
        self.project_name = project_name
        self.app_name = app_name
        self.argocd_accesstoken = get_argocdToken()
        self.host = get_argocdURI()
        self.admin = get_argocdadmin()

    def exist_app(self):
        '''
        DB 접속해서 배포할 앱이 있는지 확인
        리턴: True, False
        '''
        return ArgoUserApps.query.filter_by(project_name=self.project_name, app_name=self.app_name).first()

    def add_app(self):
        '''
        배포할 앱 등록
        1. DB 추가
        2. argocd git repo 업데이트
        '''

        # 1. db 추가
        new_app = ArgoUserApps(project_name=self.project_name, app_name=self.app_name)
        db.session.add(new_app)
        db.session.commit()

        # 2. argocd git repo 업데이트


    def trigger_deploy(self):
        '''
            argocd deploy api 호출
            리턴: argocd url
        '''
        url = ""

        try:
            data = {

            }
            headers = {}

            requests.post("", headers=headers)

        except Exception as e:
            log.error("[328] argocd deploy api 호출 실패")
        finally:
            return url

    def deploy(self):
        response = {
            'status': False,
            'deploy_url': ""
        }

        try:
            # 1. argocd 배포 DB에 앱이 등록되어 있지않으면 등록
            if not self.exist_app():
                self.add_app()
                
            # 2. argocd 앱 배포 실행
            response['deploy_url'] = self.trigger_deploy()
            response['status'] = True
            
            pass
        except Exception as e:
            log.error("[329] argocd deploy 실패")
        finally:
            return response
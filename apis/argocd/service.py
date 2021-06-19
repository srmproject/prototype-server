# -*- coding: utf-8 -*-

from config.argocd_config import get_argocdToken, get_argocdURI, get_argocdadmin, get_argocd_app_dirpath, get_appeach_values_templatepath, get_values_templatepath, get_argocd_app_valuesfile_path
import requests
from logger.log import log
import json
from .models import ArgoUserApps
from db.db import db
import requests
import chevron
import os
from git.repo.base import Repo

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
        """
            values_path: appfosapps local git repo values.yaml 경로
        """
        self.project_name = project_name
        self.app_name = app_name
        self.argocd_accesstoken = get_argocdToken()
        self.host = get_argocdURI()
        self.admin = get_argocdadmin()
        self.values_path = get_argocd_app_valuesfile_path()

    def exist_app(self):
        '''
        DB 접속해서 배포할 앱이 있는지 확인
        리턴: True, False
        '''
        return ArgoUserApps.query.filter_by(project_name=self.project_name, app_name=self.app_name).first()

    def generate_app_template(self, apps):
        '''
            argocd appofapps repo에 앱을 추가하기 위한 템플릿 생성
        '''
        try:
            apps_templates = []

            # 각 앱 템플릿 생성 후 종합
            for app in apps:
                with open(get_appeach_values_templatepath(), 'r') as f:
                    app_template = chevron.render(f, 
                        {
                            'app_name': app.app_name,
                            'project_name': app.project_name,
                        }
                    )
                apps_templates.append(app_template)
            log.debug(apps_templates)

            # 종합한 template을 appofsapps local git repo에 반영
            with open(get_values_templatepath(), 'r') as f:
                values_template = chevron.render(f, 
                    {
                        'apps': apps_templates,
                    }
                )

            with open(self.values_path, 'w') as f:
                f.write(values_template)            
        except Exception as e:
            log.error(f"[330] generate_template Error: {e}")

    def get_allapps(self):
        '''
        모든 앱 조회
        '''
        return ArgoUserApps.query.all()

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
        apps = self.get_allapps()
        self.generate_app_template(apps)
        
        # 3. git add/commit/push
        repo = Repo(get_argocd_app_dirpath())
        repo.index.add([self.values_path])
        repo.index.commit(f"add new user project.app: {self.project_name}.{self.app_name}")
        repo.git.push()

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
            log.error(f"[328] argocd deploy api 호출 실패: {e}")
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
            # response['deploy_url'] = self.trigger_deploy()
            # response['status'] = True
            
        except Exception as e:
            log.error(f"[329] argocd deploy 실패: {e}")
        finally:
            return response
# -*- coding: utf-8 -*-

from config.argocd_config import get_argocdToken, get_argocdURI, get_argocdadmin, get_argocd_app_dirpath, get_appeach_values_templatepath, get_values_templatepath, get_argocd_app_valuesfile_path, get_argocd_git_remoteurl
import requests
from logger.log import log
import json
from .models import ArgoUserApps
from db.db import db
import requests
import chevron
import os
from git.repo.base import Repo

def create_argocdapplication(argocd_host, argocd_access_token, argocd_project_name, app_name, deploy_kubernetes_namespace, app_git_remoterepo):
    """
        argocd application 생성
        파라미터:
            argocd_host: argocd 주소
            argocd_access_token: argocd 액세스 토큰
            argocd_project_name: 배포할 argocd 프로젝트 이름
            app_name: 배포할 앱 이름
            deploy_kubernetes_namespace: 배포할 쿠버네티스 namespace
            app_git_remoterepo: argocd가 배포할 앱 git 주소
        리턴:
            True: 생성성공
            False: 생성실패
    """
    try:
        response = False
        data = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": 
                { 
                    "name": f"{app_name}" 
                },
            "spec": {
                "destination": {
                    "name": "",
                    "namespace": f"{deploy_kubernetes_namespace}",
                    "server": "https://kubernetes.default.svc"
                },
                "source": {
                    "path": f"{app_name}",
                    "repoURL": f"{app_git_remoterepo}",
                    "targetRevision": "HEAD",
                    "helm": { 
                        "valueFiles": ["values.yaml"] 
                    }
                },
                "project": f"{argocd_project_name}",
                "syncPolicy": {
                    "automated": None,
                    "syncOptions": ["ApplyOutOfSyncOnly=true"]
                }
            }
        }

        request_url = """{}api/v1/applications""".format(argocd_host)
        headers = {"Authorization": "Bearer {}".format(argocd_access_token)}
        api_response = requests.post(request_url, data=json.dumps(data), headers=headers)

        if api_response.ok:
            response = True
            log.debug(f"argocd 애플리케이션 생성 성공: {argocd_project_name}")
        else:
            log.error("[332] create argocd application is failed: {}".format(api_response.json()))

    except Exception as e:
        log.error("[332] create argocd application is failed: {}".format(e))
    finally:
        return response

def exist_argocd_application(argocd_host, argocd_access_token, application_name):
    """
        argocd application 검색(모든 argocd 프로젝트 검색)
        파라미터:
            argocd_host: argocd 주소
            argocd_access_token: argocd 액세스 토큰
            application_name: 검색할 앱 이름
        리턴:
            True: 검색성공
            False: 검색실패
    """
    try:
        response = False
        
        request_url = """{}api/v1/projects/{}""".format(argocd_host, application_name)
        headers = {"Authorization": "Bearer {}".format(argocd_access_token)}
        api_response = requests.post(request_url, headers=headers)

        if api_response.ok:
            response = True
        else:
            log.error("[331] get argocd application is failed: {}".format(api_response.json()))

    except Exception as e:
        log.error("[331] get argocd application is failed: {}".format(e))
    finally:
        return response

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
            else:
                log.error("[324] create argocd project is failed: {}".format(api_response.json()))

        except Exception as e:
            log.error("[323] create argocd project: {}".format(e))
        finally:
            return response

class ArgocdappofappsApplication:
    '''
        argocd app-of-apps application관리
    '''

    def __init__(self):
        self.argocd_application_name = "app-of-apps"
        self.argocd_project = "default"
        self.argocd_gitremote_repo = get_argocd_git_remoteurl()
        self.argocd_accesstoken = get_argocdToken()
        self.argocd_host = get_argocdURI()
        self.argocd_kubernetes_namespace = "default"

    def sync(self):
        pass

    def create(self):
        """
            argocd에 app-of-apps application 생성
            리턴:
                True: 생성성공
                False: 생성실패
        """
        return create_argocdapplication(
            argocd_host=self.argocd_host,
            argocd_access_token=self.argocd_accesstoken,
            argocd_project_name=self.argocd_project,
            app_name=self.argocd_application_name,
            deploy_kubernetes_namespace=self.argocd_kubernetes_namespace,
            app_git_remoterepo=self.argocd_gitremote_repo
        )

    def is_exist(self):
        """
            argocd에 app-of-apps application이 있는지 확인
        """
        return exist_argocd_application(
            argocd_host=self.argocd_host,
            argocd_access_token=self.argocd_accesstoken,
            application_name=self.argocd_application_name
        )

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
            
            log.debug("@@@@@@@@@@@@@@@@@@@@")
            # 2. appofapps 애플리케이션이 argocd에 등록되어 있지 않으면 등록
            appofapps_helper = ArgocdappofappsApplication()
            if not appofapps_helper.is_exist():
                appofapps_helper.create()

            # 3. appofapps 애플리케이션 sync
            # appofapps_helper.sync()
            
        except Exception as e:
            log.error(f"[329] argocd deploy 실패: {e}")
        finally:
            return response
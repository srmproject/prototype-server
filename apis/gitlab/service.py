# -*- coding: utf-8 -*-
from abc import *
import requests
from urllib.parse import urljoin
from logger.log import log
from apis.auth.models import User
from apis.auth.service import get_userByEmail
from config.gitlab_config import get_GitlabAccessToken, get_GitlabInitPassword, get_gitlabURI, get_default_memberexpires_data
from .models import ServiceProject, UserProjectMappingEntity, ServiceApp, UserAppMappingEntity
from db.db import db
from apis.auth.models import GitlabUser
from config.gitlab_config import get_pythonappId, get_springbootappId
from flask_login import current_user
from apis.jenkins.service import JenkinsCreateFolder, JenkinsCreateJob
from apis.jenkins.models import JenkinsJob
from config.helm_config import get_default_cpu, get_default_memory, get_springboot_helmurl
from apis.helm.service import HelmCreateUserApp
from apis.argocd.service import ArgocdCreateProject

class AbstractGitlab(metaclass=ABCMeta):
    '''
        gitlab서비스클래스 추상화
    '''

    # gitlab API를 사용하기 위한 accesstoekn 설정
    accesstoken = get_GitlabAccessToken() # this is for sample
    gitlabURI = get_gitlabURI()
    initpassword = get_GitlabInitPassword()
    
    @abstractmethod
    def createGroup(self, post_data, requsetuser_information):
        '''
            그룹 생성
            파라미터:
                post_data: CreateGroupRequestDto class.__dict__
                requsetuser_information: 프로젝트 생성 요청자의 이메일
        '''
        pass

    @abstractmethod
    def getUsers(self):
        '''
            gitlab 계정목록 조회
        '''
        pass

    def addMembersToGroup(self, group_id, gitlabuser_id):
        '''
            Group 멤버 추가
            파라미터:
                group_id: gitlab group ID
                user_id: gitlab user_id
        '''    
        pass

    def getUserByflaskuserID(self, flaskuser_id):
        '''
            flask userid로 gitlab user조회
        '''
        pass

    def createApp(self, createAppRequestDto):
        '''
            앱 생성
        '''
        pass

class GitlabImpl(AbstractGitlab):
    def __init__(self):
        pass

    def createGroup(self, post_data, requsetuser_information):
        '''
            프로젝트 생성
                gitlab group 생성, 젠킨스 폴더 생성, argocd 프로젝트 생성
            파라미터:
                post_data: CreateGroupRequestDto class.__dict__
                requsetuser_information: 프로젝트 생성 요청자의 이메일
        '''

        URI = urljoin(self.gitlabURI, "groups")
        headers = {"Authorization": "Bearer {}".format(self.accesstoken)}

        result = {
            'status': False,
            'data': None
        }

        try:
            
            api_response = requests.post(URI, headers=headers, data=post_data)
            result['status'] = api_response.ok

            if not result['status']:
                log.error('[Error 311] gitlab 그룹 생성 실패')
            else:
                log.debug("[debug 001] {} 그룹생성 성공".format(post_data['name']))
                
                # 젠킨스 폴더 생성
                jenkinscreatefolder = JenkinsCreateFolder(post_data['name'])
                create_jenkinsfolder_response = jenkinscreatefolder.create()
                                
                if create_jenkinsfolder_response['status']:
                    # argocd 프로젝트 생성
                    argocdcontroller = ArgocdCreateProject(post_data['name'])
                    argocd_response = argocdcontroller.create()
                    if argocd_response:
                        # 생성한 프로젝트 db 등록
                        # 젠킨스 폴더, argocd를 따로 관리하는 DB는 없음
                        result['data'] = api_response.json()                        
                        login_user = get_userByEmail(requsetuser_information)

                        project = ServiceProject(result['data']['id'], result['data']['web_url'], result['data']['name'])
                        db.session.add(project)
                        db.session.commit()
                        
                        user_project_mapping = UserProjectMappingEntity(flaskuser_id=login_user.id, project_id=project.id)
                        db.session.add(user_project_mapping)
                        db.session.commit()

                        gitlabuser = self.getUserByflaskuserID(login_user.id)
                        self.addMembersToGroup(result['data']['id'], gitlabuser.gitlab_userid)
                        
                        result['status'] = True
                        log.info("그룹{} DB 등록 성공".format(post_data['name']))

        except Exception as e:
            log.error("[Error 310] gitlab 그룹생성 실패: {}".format(e))
        finally:
            return result

    def addMembersToGroup(self, group_id, gitlabuser_id):
        '''
            Group 멤버 추가
            파라미터:
                group_id: gitlab group ID
                user_id: gitlab user_id
        '''

        result = False

        try:
            
            URI = urljoin(self.gitlabURI, "groups/{}/members".format(group_id))
            headers = {"Authorization": "Bearer {}".format(self.accesstoken)}
            
            data = {
                "id": group_id,
                "user_id": gitlabuser_id,
                "access_level": "30",
                "expires_at": get_default_memberexpires_data()
            }

            api_response = requests.post(URI, headers=headers, data=data)
            
            if api_response.ok:
                result = True

        except Exception as e:
            log.error("[Erorr 312] gitlab Group에 계정추가 실패 :{}".format(e))

        return result

    def existUser(self, email):
        '''
            flask user가 존재하는지 확인
        '''
        log.debug("---------------------")
        log.debug(email)
        return User.query.filter_by(email=email).first()

    def existGitlabUser(self):
        '''
            gitlab User가 존재하는지 확인
        '''
        pass
    
    def getUsers(self):
        '''
            gitlab 계정목록 조회
        '''
        
        response = {
            'status': False,
            'data': []
        }

        try:
            URI = urljoin(self.gitlabURI, "users")
            headers = {"Authorization": "Bearer {}".format(self.accesstoken)}
            api_response = requests.get(URI, headers=headers)
            
            response['status'] = api_response.ok

            if not response['status']:
                log.debug('[Error 301] 계정목록 조회실패. 응답코드: {}'.format(response['status']))
            else:
                log.debug("[OK] 계정목록 조회 성공")
                response['data'] = api_response.json()

        except Exception as e:
            log.error('[Error 300] 계정목록 조회실패: {}'.format(e))

        return response

    def getUserByflaskuserID(self, flaskuser_id):
        '''
            flask userid로 gitlab user조회
        '''
        return GitlabUser.query.filter_by(user_id=flaskuser_id).first()

    def createApp(self, createAppRequestDto):
        '''
            앱 생성
                1. gitlab 템플릿 fork
                2. helm템플릿 디렉터리를 생성하고 argocd git repo에 push
                3. jenkins job 생성
        '''
        result = {
            'status': False,
            'data': None
        }
        try:
            # helm_projectId = ""
            # helm 템플릿 컨테이너 포트
            helm_values_port = 80
            helm_downloadurl = ""

            # fork할 애플리케이션 정보 초기화
            if createAppRequestDto['id'] == "python":
                createAppRequestDto['id'] = get_pythonappId()
                helm_values_port = 5000
            elif createAppRequestDto['id'] == "springboot":
                createAppRequestDto['id'] = get_springbootappId()
                # helm_projectId = get_springboot_helm_rootId()
                helm_values_port = 8080
                helm_downloadurl = get_springboot_helmurl()

            # 1. 애플리케이션 gitlab 프로젝트 fork
            log.debug("fork application gitlab project start")
            service_projectid = createAppRequestDto['namespace_id']
            find_serviceproject = ServiceProject.query.filter_by(id=createAppRequestDto['namespace_id']).first()
            selected_group_id = find_serviceproject.project_id
            # selected_group_name = find_serviceproject.project_name
            createAppRequestDto['namespace_id'] = selected_group_id
            
            gitlab_URI = f"{self.gitlabURI}projects/{createAppRequestDto['id']}/fork"
            headers = {"Authorization": "Bearer {}".format(self.accesstoken)}
            api_response = requests.post(gitlab_URI, headers=headers, data=createAppRequestDto)
            log.debug("fork application gitlab project done")

            if api_response.ok:
                api_response_data = api_response.json()
                
                # 2. 애플리케이션 helm 디렉터리 생성과 argocd git repo에 push
                log.debug("create helm template and push gitrepo start")

                helmApp = HelmCreateUserApp(
                                            # helm_repo_url=helm_response['http_url_to_repo'],
                                            helm_downloadurl=helm_downloadurl,
                                            application_name=createAppRequestDto['name'],
                                            cpu=get_default_cpu(),
                                            memory=get_default_memory(),
                                            port=helm_values_port,
                                            image_version="dev"
                                        )
                helmApp.create()
                log.debug("create helm template and push gitrepo done")

                # 3. 젠킨스 잡 생성
                jenkinsCreateJob = JenkinsCreateJob(job_name=createAppRequestDto['name'],
                                                    folder_name=find_serviceproject.project_name,
                                                    git_repo_url=api_response_data['http_url_to_repo'])
                jenkinsjob_create_result = jenkinsCreateJob.createJobWithFolder()

                if jenkinsjob_create_result['status'] and jenkinsjob_create_result['data']['token']:
                    login_user = get_userByEmail(current_user.email)

                    # db 등록
                    # 1. service app 등록
                    new_serviceapp = ServiceApp(project_id=api_response_data['id'],
                                                project_name=api_response_data['name'],
                                                weburl=api_response_data['web_url'],
                                                group_id=service_projectid,
                                                git_repo_url=api_response_data['http_url_to_repo'])

                    log.debug(new_serviceapp.__dict__)
                    db.session.add(new_serviceapp)
                    db.session.commit()

                    # 2. user_servicempping 등록
                    new_userappmapping = UserAppMappingEntity(flaskuser_id=login_user.id, app_id=new_serviceapp.id)
                    db.session.add(new_userappmapping)
                    db.session.commit()

                    # 3. 젠킨스 db 등록
                    new_jenkinsjob = JenkinsJob(
                        app_id=new_serviceapp.id,
                        job_name=new_serviceapp.project_name,
                        token=jenkinsjob_create_result['data']['token']
                    )
                    db.session.add(new_jenkinsjob)
                    db.session.commit()

                    result['status'] = True
                    result['data'] = api_response_data

                    log.debug("fork 성공")
                else:
                    log.error("[325] jenkins job 생성 실패: {}".format(jenkinsjob_create_result.json()))
        except Exception as e:
            log.error("[Error 315] git fork 실패: {}".format(e))

        return result

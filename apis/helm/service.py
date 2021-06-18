# -*- coding: utf-8 -*-
import zipfile
from logger.log import log
import chevron
from git.repo.base import Repo
import os
import stat
from config.gitlab_config import get_GitlabAccessToken, get_GitlabInitPassword, get_gitlabURI, get_default_memberexpires_data
from config.argocd_config import get_argocd_app_dirpath, get_argocd_app_groupname, get_argocd_app_name
import time
from urllib.request import urlopen
from zipfile import ZipFile
import os
from pathlib import Path
import urllib

def change_rootdir(zipinfo_filename, to_changename):
    """
        압축을 해제할 때 rootdir 이름 변경
    """

    split_name = zipinfo_filename.split("/")
    split_name[0] = to_changename

    return "/".join(split_name)

def download_and_unzip_helmtemplate(url, download_path, uznip_path, app_name):
    """
        헬름 템플릿을 다운로드 받고 압축해제
    """
    try:
        urllib.request.urlretrieve(url, download_path)
        
        # 임시 디렉터리로 압축해제
        unzip_path = download_path.split('.zip')[0]

        with zipfile.ZipFile(download_path) as zipobj:
            zipinfos = zipobj.infolist()
            for zipinfo in zipinfos:
                zipinfo.filename = change_rootdir(zipinfo.filename, app_name)
                log.debug("zipinfo:{}".format(zipinfo.filename))
                zipobj.extract(zipinfo, uznip_path)
    except Exception as e:
        log.error("[327] donwload helm template: {}".format(e))

def readonly_handler(func, path, execinfo):
    '''
        git 프로젝트 삭제 에러 핸들링
    '''
    os.chmod(path, stat.S_IWRITE)
    func(path)

class HelmCreateUserApp:
    '''
        helm gitlab 프로젝트 생성
        애플리케이션 생성 과정에서 helm 호출
    '''

    def __init__(self, helm_downloadurl, application_name, cpu, memory, port, image_version=1):
        # self.helm_repo_url = helm_repo_url
        self.helm_download_url = helm_downloadurl
        self.image_name = application_name
        self.helm_localpath = os.path.join(get_argocd_app_dirpath(), application_name)
        self.imgae_version = image_version
        self.port = port
        self.helm_values_path = os.path.join(self.helm_localpath, 'values.yaml')
        self.cpu = cpu
        self.memory = memory
        self.timeout = 5
    
    def create(self):
        '''
            app helm 생성후 argocd repo에 push
                values.yaml수정
        '''
        # wait fork helm project done
        time.sleep(5)

        try:
            log.debug(f"helm downloadurl: {self.helm_download_url}")
            log.debug(f"dst : {self.helm_localpath}")

            download_and_unzip_helmtemplate(
                self.helm_download_url, 
                download_path=f"{self.helm_localpath}.zip",
                uznip_path=Path(self.helm_localpath).parent,
                app_name=self.image_name
            )

            # 2. change helm valeus.yaml
            with open(self.helm_values_path, 'r') as f:
                changed = chevron.render(f, 
                    {
                        "IMAGENAME": self.image_name,
                        "IMAGETAG": self.imgae_version,
                        "PORT": self.port,
                        "CPU": self.cpu,
                        "MEMORY": self.memory
                    }
                )            
            with open(self.helm_values_path, 'w') as f:
                f.write(changed)
            log.debug("change values.yaml done")

            # 4. add, commit and push
            repo = Repo(get_argocd_app_dirpath())
            repo.index.add(['values.yaml'])
            repo.index.commit(f"add new user app: {self.image_name}")
            log.debug("{} helm add and commit done".format(self.helm_localpath))

            repo.git.push()
            log.debug("{} helm push done".format(self.helm_localpath))

            # 5. delete local helm project
            # self.delete_local_helmproject()
            
        except Exception as e:
            log.error("[318] create app helm is failed {}".format(e))
            # gitlab project 생성대기
            raise("[318] create app helm is failed {}".format(e))
            
    # def delete_local_helmproject(self):
    #     '''
    #         helm local프로젝트 삭제
    #     '''
    #     if os.path.exists(self.helm_localpath):
    #         #reference: https://programmersought.com/article/97605598037/
    #         shutil.rmtree(self.helm_localpath, onerror=readonly_handler)

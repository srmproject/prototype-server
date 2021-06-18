# -*- coding: utf-8 -*-

from config.argocd_config import get_argocdToken, get_argocdURI, get_argocdadmin
import requests
from logger.log import log
import json

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
        argocd 앱 배포
    """

    def __init__(self):
        pass
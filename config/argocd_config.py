import yaml
from pathlib import Path
import os

def get_argocdadmin():
    '''
        리턴: argocd admin계정
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['argocd']['admin_user']

def get_argocdToken():
    '''
        리턴: argocd accesstoekn 설정
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['argocd']['access_token']

def get_argocdURI():
    '''
        리턴: argocdURI
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['argocd']['host']

def get_argocd_app_dirpath():
    '''
        리턴: 사용자 앱 관리 git repo
            디폴트: 홈디렉터리
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # 사용자 앱 관리 git repo
    gitrepo_name = Path(config['argocd']['git_repo']['app']['name'])
    
    return os.path.join(Path.home(), gitrepo_name)
    
def get_argocd_app_groupname():
    '''
        리턴: 사용자 앱 관리 git repo group이름
            디폴트: 홈디렉터리
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['argocd']['git_repo']['app']['group_name']

def get_argocd_app_name():
    '''
        리턴: 사용자 앱 관리 git repo group이름
            디폴트: 홈디렉터리
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['argocd']['git_repo']['app']['name']
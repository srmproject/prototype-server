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

def get_argocd_app_valuesfile_path():
    '''
        리턴: 사용자 앱 관리 git repo values 경로
            디폴트: 홈디렉터리
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # 사용자 앱 관리 values.yaml 경로
    return os.path.join(get_argocd_app_dirpath(), 'app-of-apps', 'values.yaml')
    
def get_argocd_app_groupname():
    '''
        리턴: 사용자 앱 관리 git repo group이름
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['argocd']['git_repo']['app']['group_name']

def get_argocd_app_name():
    '''
        리턴: 사용자 앱 관리 git repo group이름
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['argocd']['git_repo']['app']['name']

def get_appeach_values_templatepath():
    '''
        리턴: 사용자 앱 관리 git repo group이름
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return os.path.join('config', config['argocd']['templates']['values_each_template_path'])

def get_values_templatepath():
    '''
        리턴: 사용자 앱 관리 git repo group이름
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return os.path.join('config', config['argocd']['templates']['values_template_path'])

def get_argocd_git_remoteurl():
    '''
        리턴: argocd app-of-apps git remote url
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['argocd']['git_repo']['remote_url']
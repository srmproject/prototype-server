import yaml

from config.gitlab_config import get_gitlabHost

def get_springboot_helm_rootId():
    '''
        리턴: helm springboot helm project ID
    '''

    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['helm']['springboot']['app_gitlab_projectid']

def get_common_helm():
    '''
        리턴: helm common project
    '''

    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['helm']['common_helm_groupId']

def get_default_cpu():
    '''
        리턴: helm default cpu
    '''

    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['helm']['default_resources']['cpu']

def get_default_memory():
    '''
        리턴: helm default cpu
    '''

    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['helm']['default_resources']['memeory']

def get_springboot_helmprojectname():
    '''
        리턴: springboot helm 프로젝트 이름
    '''

    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['helm']['springboot']['helm_gitlab_projectname']


def get_springboot_helmurl():
    '''
        리턴: 스프링부트 helm 다운로드 url
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    url = config['helm']['springboot']['helm_gitlab_groupurl']

    return "{}{}/{}/-/archive/master/{}-master.zip".format(
                get_gitlabHost(),
                url,
                get_springboot_helmprojectname(),
                get_springboot_helmprojectname()
            )
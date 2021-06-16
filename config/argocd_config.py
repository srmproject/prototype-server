import yaml

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

    
import yaml

def get_private_dockerregistry_host():
    '''
        리턴: privat docker registry 주소
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['docker']['prviate_registry_host']

def get_private_dockerregistry_protocol():
    '''
        리턴: privat docker registry 주소
    '''
    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['docker']['protocol']
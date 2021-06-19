import yaml
import os

def get_grafana_host():
    '''
        리턴: 그라파나 host
    '''

    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return config['grafana']['host']

def get_grafana_dashboard_templatepath():
    '''
        리턴: 그라파나 대시보드 템플릿 경로
    '''

    with open('config/global_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    return os.path.join('config', config['grafana']['dashboard_filterpath'])

    
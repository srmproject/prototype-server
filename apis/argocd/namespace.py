from flask_restx import Resource, Namespace
from logger.log import log
from werkzeug.utils import redirect
from apis.argocd.service import ArgocdDeploy
from config.argocd_config import get_argocdURI
from urllib.parse import urljoin

ns = Namespace('argocd', version="1.0", description='argocd controller')

@ns.route("/healthcheck")
class Index(Resource):
    @ns.doc(response={200: "success"})
    def get(self):
        return "This is a argocd health check api"

@ns.route("/deploy/<string:project_name>/<string:app_name>")
class Index(Resource):
    '''
        앱 배포
    '''
    @ns.doc(response={200: "success"})
    def get(self, project_name, app_name):
        argocd_url = urljoin(get_argocdURI(), f"applications/{project_name}-{app_name}")
        argocddeploy = ArgocdDeploy(project_name, app_name)
        argocddeploy.deploy()
        log.debug(f"argocd_url: {argocd_url}")
        return redirect(argocd_url)

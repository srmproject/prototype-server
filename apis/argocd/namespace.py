from flask_restx import Resource, Namespace
from logger.log import log
from werkzeug.utils import redirect

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
        return f"{project_name}, {app_name}"

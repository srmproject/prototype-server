from flask_restx import Resource, Namespace
from logger.log import log
from .service import JenkinsTriggerJob
from werkzeug.utils import redirect

ns = Namespace('argocd', version="1.0", description='argocd controller')

@ns.route("/healthcheck")
class Index(Resource):
    @ns.doc(response={200: "success"})
    def get(self):
        return "This is a argocd health check api"


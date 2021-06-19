from flask_restx import Resource, Namespace
from werkzeug.utils import redirect
from urllib.parse import urljoin
from config.grafana_config import get_grafana_host, get_grafana_dashboard_templatepath
import chevron

ns = Namespace('grafana', version="1.0", description='grafana controller')

@ns.route("/log/<string:project_name>/<string:app_name>")
class Index(Resource):
    '''
        앱 배포
    '''
    @ns.doc(response={200: "success"})
    def get(self, project_name, app_name):

        with open(get_grafana_dashboard_templatepath(), "r", encoding="utf-8") as f:
            grafana_filter = chevron.render(f.readline(), {
                "project_name": project_name,
                "app_name": f"{project_name}-{app_name}"
            })

        grafana_dashboard_url = urljoin(get_grafana_host(), "/explore?orgId=1&left={}".format(grafana_filter))

        return redirect(grafana_dashboard_url)

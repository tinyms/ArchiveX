__author__ = 'tinyms'
from tinyms.core.web import IAuthRequest
from tinyms.core.point import route

@route("/workbench/dashboard")
class Workbench(IAuthRequest):
    def get(self, *args, **kwargs):
        self.render("workbench/dashboard.html")
    def post(self, *args, **kwargs):
        self.render("workbench/dashboard.html")
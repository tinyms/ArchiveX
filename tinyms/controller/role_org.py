__author__ = 'tinyms'

from tinyms.core.web import IAuthRequest
from tinyms.core.point import route

@route("/workbench/security")
class RoleOrg(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/role_org.html")

__author__ = 'tinyms'

from tinyms.core.web import IAuthRequest
from tinyms.core.point import route

@route("/workbench/setting")
class SettingPage(IAuthRequest):

    def get(self, *args, **kwargs):
        return self.render("workbench/setting.html")
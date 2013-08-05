__author__ = 'Administrator'
__export__ = ["Welcome"]

from tinyms.web import IRequest
from tinyms.point import IWebConfig

class Welcome(IWebConfig):

    def url_mapping(self,url_patterns):
        url_patterns.append((r"/",WelcomeHandler))
        pass

class WelcomeHandler(IRequest):
    def get(self):
        self.redirect("/static/index.html")
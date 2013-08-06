__author__ = 'tinyms'
__export__ = ["Welcome"]

import urllib.request
from tinyms.web import IRequest
from tinyms.point import IWebConfig
from tinyms.common import Utils

class Welcome(IWebConfig):

    def url_mapping(self,url_patterns):
        url_patterns.append((r"/",WelcomeHandler))
        pass

class WelcomeHandler(IRequest):
    def get(self):
        web_page = urllib.request.urlopen("http://trade.500.com/bjdc/",timeout=15)
        html = web_page.read()
        html = html.decode('gb18030')
        Utils.text_write("cache",[html])
        self.redirect("/static/index.html")
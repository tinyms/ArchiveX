__author__ = 'tinyms'
__export__ = ["Welcome"]

from tinyms.web import IRequest
from tinyms.point import IWebConfig, IApi
from lottery.parse import MatchAnalyzeThread


class Welcome(IWebConfig):
    def url_mapping(self, url_patterns):
        url_patterns.append((r"/", WelcomeHandler))
        pass


class WelcomeHandler(IRequest):
    def get(self):
        self.redirect("/static/index.html")

#/api/welcome.MatchAnalyze/run
class MatchAnalyze(IApi):
    __export__ = ["run"]
    thread = None

    def run(self, **p):
        msg = dict()
        if not MatchAnalyzeThread.IS_RUNNING:
            MatchAnalyze.thread = MatchAnalyzeThread()
            MatchAnalyze.thread.urls = [p["url"]]
            MatchAnalyze.thread.start()
            msg["msg"] = "启动分析成功"
        else:
            msg["msg"] = "分析进行中"
        return msg
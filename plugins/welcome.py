__author__ = 'tinyms'
__export__ = ["Welcome", "MatchAnalyze"]

import os, json
from tinyms.web import IRequest
from tinyms.common import Utils
from tinyms.point import IWebConfig, IApi
from lottery.parse import MatchAnalyzeThread


class Welcome(IWebConfig):
    def url_mapping(self, url_patterns):
        url_patterns.append((r"/", WelcomeHandler))
        pass


class WelcomeHandler(IRequest):
    def get(self):
        self.redirect("/static/index.html")

#/api/welcome.MatchAnalyze/method
class MatchAnalyze(IApi):
    __export__ = ["run", "result"]
    thread = None

    def result(self, **p):
        msg = dict()
        if not p["url"]:
            msg["msg"] = "NotBlank"
            return msg
        if not Utils.url_with_params(p["url"]):
            msg["msg"] = "UrlRequireParams."
            return msg
        file = "cache_web_pages/%s.json" % Utils.md5(Utils.trim(p["url"]))
        if not os.path.exists(file):
            return list()
        else:
            content = Utils.text_read(file)
            return json.loads(content)

    def run(self, **p):
        msg = dict()
        act = p["act"];
        file = "cache_web_pages/%s.json" % Utils.md5(Utils.trim(p["url"]))
        print(act)
        if act=="Refresh":
            dataset = json.loads(Utils.text_read(file))
            for item in dataset:
                id = item["match_id"]
                odds_url_cache_file = "http://odds.500.com/fenxi/ouzhi-%i" % id
                os.remove("cache_web_pages/"+Utils.md5(odds_url_cache_file))
                print(odds_url_cache_file)
            os.remove(file)

        if os.path.exists(file):
            msg["msg"] = "History"
            return msg
        if not p["url"]:
            msg["msg"] = "NotBlank"
            return msg
        if not Utils.url_with_params(p["url"]):
            msg["msg"] = "UrlRequireParams."
            return msg
        if not MatchAnalyzeThread.IS_RUNNING:
            MatchAnalyze.thread = MatchAnalyzeThread()
            MatchAnalyze.thread.urls = [p["url"]]
            MatchAnalyze.thread.start()
            msg["msg"] = "Started"
        else:
            msg["msg"] = "Running"
        return msg
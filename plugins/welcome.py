__author__ = 'tinyms'
__export__ = ["Welcome", "MatchAnalyze","MatchHistoryQuery"]

import os, json
from tinyms.web import IRequest
from tinyms.common import Utils
from tinyms.point import IWebConfig, IApi, IAjax
from tinyms.common import Postgres
from lottery.parse import MatchAnalyzeThread


class Welcome(IWebConfig):
    def url_mapping(self, url_patterns):
        url_patterns.append((r"/", WelcomeHandler))
        pass


class WelcomeHandler(IRequest):
    def get(self):
        self.redirect("/static/index.html")

class MatchHistoryQuery(IAjax):
    __export__ = ["find"]

    def client_javascript_object_name(self):
        return "WelcomeMatchHistoryQuery"

    def find(self,**p):
        force = p["force"]
        win_direct = p["win_direct"]
        company = p["company"]
        draw_ext = p["draw_ext"]
        draw_change_direct = p["draw_change_direct"]
        draw_range = p["draw_range"]
        sql = "select * from matchs where detect_result = '%s'" % force
        col = "Odds_%s" % company

        nums = Utils.parse_float_array(draw_ext)
        if len(nums)==1:
            sql += " AND (%s[2]-trunc(%s[2]))=%.2f" % (col,col,nums[0])

        nums = Utils.parse_float_array(draw_range)
        if len(nums)==1 and nums[0]>0:
            sql += " AND (abs(%s_c[2]-%s[2])>=%.2f AND abs(%s_c[2]-%s[2])<=%.2f)" % (col,col,nums[0],col,col,nums[0]+0.1)

        if draw_change_direct=="gt":
            sql += " AND %s_c[2]-%s[2] > 0" % (col,col)
        elif draw_change_direct=="lt":
            sql += " AND %s_c[2]-%s[2] < 0" % (col,col)

        if win_direct == "3":
            sql += " AND %s[1]-%s[3]<0"  % (col,col)
        elif win_direct == "0":
            sql += " AND %s[1]-%s[3]>0"  % (col,col)
        else:
            sql += " AND %s[1]-%s[3]=0" % (col,col)

        result = dict()
        result["win"] = self.count_matchs(sql,3)
        result["draw"] = self.count_matchs(sql,1)
        result["lost"] = self.count_matchs(sql,0)
        print(result)
        return self.json(result)

    def count_matchs(self,sql,act_result):
        result = dict()
        sql += " AND actual_result = %i" % act_result
        count_sql = sql.replace("*","COUNT(1)")
        sql += " ORDER BY random() LIMIT 50"
        result["total"] = Postgres.one(count_sql)
        result["items"] = Postgres.many(sql)
        return result

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
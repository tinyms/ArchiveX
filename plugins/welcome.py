__author__ = 'tinyms'
__export__ = ["Welcome", "MatchAnalyze","MatchHistoryQuery","SingleOrder"]

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

class SingleOrder(IAjax):
    __export__ = ["create"]

    def client_javascript_object_name(self):
        return "SingleOrderComposite"

    def compare_two(self,a_arr,b_arr):
        size = len(a_arr)
        if size != len(a_arr):
            return -1
        count = 0
        for i in range(size):
            if a_arr[i] != b_arr[i]:
                count += 1
        return count

    def color(self,result):
        html = result.replace("3","<button style='margin-left:5px;' type='button' class='btn btn-primary'>3</button>")
        html = html.replace("1","<button style='margin-left:5px;' type='button' class='btn btn-success'>1</button>")
        html = html.replace("0","<button style='margin-left:5px;' type='button' class='btn btn-danger'>0</button>")
        return html

    def create(self,**p):
        num = Utils.parse_int(p["num"])
        maybe_err = Utils.parse_int(p["err"])
        source = p["source"]
        if source:
            items = [s.strip(" ") for s in source.split(",")]
            import itertools,random
            a = list(itertools.product(*items))
            first = a[0]
            result = list()
            for r in a:
                diff = self.compare_two(first,r)
                if diff == maybe_err:
                    result.append("".join(r))
            random.shuffle(result)
            random.shuffle(result)
            result.insert(0,"".join(first))
            color_result = list()
            for sr in result:
                color_result.append(self.color(sr))
        ds = dict()
        ds["result"] = result[:num]
        ds["color_result"] = color_result[:num]
        return self.json(ds)

class MatchHistoryQuery(IAjax):
    __export__ = ["find"]

    def client_javascript_object_name(self):
        return "WelcomeMatchHistoryQuery"

    def find(self,**p):
        force = p["force"]
        win_direct = p["win_direct"]
        company = p["company"]
        draw_ext = p["draw_ext"]
        odds_win = p["odds_win"];
        sql = "select * from matchs where detect_result = '%s'" % force
        col = "Odds_%s" % company

        nums = Utils.parse_float_array(draw_ext)
        if len(nums)==1:
            sql += " AND (%s[2]-trunc(%s[2]))=%.2f" % (col,col,nums[0])

        nums = Utils.parse_float_array(odds_win)
        if len(nums)==1:
            if win_direct == "3":
                sql += " AND (%s[1]>%.2f AND %s[1]<%.2f)" % (col,nums[0]-0.2,col,nums[0]+0.2)
            else:
                sql += " AND (%s[3]>%.2f AND %s[3]<%.2f)" % (col,nums[0]-0.2,col,nums[0]+0.2)

        if win_direct == "3":
            sql += " AND actual_result=3"
        elif win_direct == "0":
            sql += " AND actual_result=0"
        else:
            sql += " AND actual_result=1"
        print(sql)
        result = dict()
        result["win"] = self.count_matchs(sql,3)
        result["draw"] = self.count_matchs(sql,1)
        result["lost"] = self.count_matchs(sql,0)
        return self.json(result)

    def count_matchs(self,sql,act_result):
        result = dict()
        sql += " AND actual_result = %i" % act_result
        count_sql = sql.replace("*","COUNT(1)")
        sql += " ORDER BY random() LIMIT 25"
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
        if act=="Refresh" and os.path.exists(file):
            dataset = json.loads(Utils.text_read(file))
            for item in dataset:
                id = item["match_id"]
                odds_url_cache_file = "http://odds.500.com/fenxi/ouzhi-%i" % id
                os.remove("cache_web_pages/"+Utils.md5(odds_url_cache_file))
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
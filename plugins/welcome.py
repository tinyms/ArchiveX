__author__ = 'tinyms'
__export__ = ["MatchAnalyze","MatchHistoryQuery","SingleOrder"]

import os, json
from tinyms.web import IRequest,route
from tinyms.common import Utils
from tinyms.point import IAjax, api, ajax
from tinyms.common import Postgres
from lottery.parse import MatchAnalyzeThread


@route(r"/ui/test")
class UITestHandler(IRequest):
    def get(self):
        self.render("ui.html")

@api("test")
class ApiTest():
    def list(self):
        print(self.param("abc"))
        return [2,5,1,12]

@ajax("test")
class AjaxTest():
    __export__ = ["list"]
    def list(self):
        print(self.param("abc"))
        return [2,5,1,12]

@route(r"/")
class WelcomeHandler(IRequest):
    def get(self):
        self.redirect("/static/index.html")

@ajax("single_order")
class SingleOrder():
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

    def results_balance(self,normal_result_arr):
        rcv = [[r[col] for r in normal_result_arr] for col in range(len(normal_result_arr[0]))]
        items = []
        for r in rcv:
            items.append("".join(r))
        counters = []
        for item in items:
            counter = {}
            for c in item:
                if c in counter:
                    counter[c] += 1
                else:
                    counter[c] = 1
            fmt = "('%s',%i)"
            tmp = sorted([(v,k) for v,k in counter.items()],reverse=True)
            tmp_texts = ""
            for t in tmp:
                tmp_texts += fmt % (t[0],t[1])
            counters.append(tmp_texts)
        return counters

    def create(self):
        num = Utils.parse_int(self.param("num"))
        maybe_err = Utils.parse_int(self.param("err"))
        source = self.param("source")
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
        #统计赛果比例
        result_for_rate = list()
        for item in ds["result"]:
            result_for_rate.append([s for s in item])
        ds["balance"] = self.results_balance(result_for_rate)
        return ds

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

        nums = Utils.parse_number_array(odds_win)
        if len(nums)==1:
            if nums[0] >= 0:
                sql += " AND (%s[1]>%.2f AND %s[1]<%.2f)" % (col,abs(nums[0])-0.2,col,abs(nums[0])+0.2)
            else:
                sql += " AND (%s[3]>%.2f AND %s[3]<%.2f)" % (col,abs(nums[0])-0.2,col,abs(nums[0])+0.2)

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
@api("match_analyze")
class MatchAnalyze():

    thread = None

    def result(self):
        msg = dict()
        url = self.param("url")
        if not url:
            msg["msg"] = "NotBlank"
            return msg
        if not Utils.url_with_params(url):
            msg["msg"] = "UrlRequireParams."
            return msg
        file = "cache_web_pages/%s.json" % Utils.md5(Utils.trim(url))
        if not os.path.exists(file):
            return list()
        else:
            content = Utils.text_read(file)
            return json.loads(content)

    def run(self):
        msg = dict()
        act = self.param("act")
        url = self.param("url")
        file = "cache_web_pages/%s.json" % Utils.md5(Utils.trim(url))
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
        if not url:
            msg["msg"] = "NotBlank"
            return msg
        if not Utils.url_with_params(url):
            msg["msg"] = "UrlRequireParams."
            return msg
        if not MatchAnalyzeThread.IS_RUNNING:
            MatchAnalyze.thread = MatchAnalyzeThread()
            MatchAnalyze.thread.urls = [url]
            MatchAnalyze.thread.start()
            msg["msg"] = "Started"
        else:
            msg["msg"] = "Running"
        return msg
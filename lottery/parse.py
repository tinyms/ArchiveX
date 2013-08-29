__author__ = 'tinyms'

import sys
import os, threading
import re
import random, json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from tinyms.common import Utils
from tinyms.orm import SessionFactory

from lottery.formula import Formula
from lottery.entity import Battle,Odds


class MatchAnalyzeThread(threading.Thread):
    IS_RUNNING = False
    IS_HISTORY = False
    def __init__(self):
        threading.Thread.__init__(self)
        self.urls = list()
        self.cached = False

    def run(self):
        MatchAnalyzeThread.IS_RUNNING = True
        for url in self.urls:
            ds = MatchAnalyzeThread.extract_matchs([url], self.cached)
            MatchAnalyzeThread.parse(ds)
        MatchAnalyzeThread.IS_RUNNING = False

    @staticmethod
    def extract_matchs(urls, cached=False):
        #make dir
        Utils.mkdirs("cache_web_pages")
        data = list()
        for url in urls:
            if cached:
                Helper.web_page_download(url, cached)
                soup = Helper.soup(Helper.cache_file_name(url))
            else:
                soup = Helper.soup(url, False)
            if not soup:
                print("Soup None.")
                continue
            trNodes = soup.find_all("tr")
            season_no = Utils.md5(Utils.trim(url))
            for tr in trNodes:
                match_item = dict()
                match_item["score"] = ""
                match_item["result"] = -1
                match_item["season_no"] = season_no
                linkNodes = tr.find_all("a")
                alive_result = []
                for link in linkNodes:
                    href = link["href"]
                    if href.find("seasonindex") != -1:
                        match_item["season_name"] = Utils.trim(link.get_text())
                    elif href.find("teamid") != -1:
                        if match_item.get("team_names"):
                            match_item["team_names"] += " VS " + Utils.trim(link.get_text())
                        else:
                            match_item["team_names"] = Utils.trim(link.get_text())
                    elif href.find("/fenxi/shuju") != -1:
                        match_item["match_id"] = abs(Utils.parse_int_array(href)[1])
                        map_ = MatchAnalyzeThread.get_actual_result(link.get_text())
                        match_item["score"] = "[%s]" % map_["exp"]
                        match_item["actual_result"] = "%i" % map_["result"]
                    elif href.find("detail.php?fid=") != -1 and link.string:
                        nums = Utils.parse_int_array(link.get_text())
                        if len(nums) != 0:
                            alive_result.append(nums[0])
                if len(alive_result) == 2:
                    r = alive_result[0] - alive_result[1]
                    if r > 0:
                        result = 3
                    elif r == 0:
                        result = 1
                    else:
                        result = 0
                    match_item["score"] = "[%i:%i]" % (alive_result[0], alive_result[1])
                    match_item["actual_result"] = "%i" % result
                if match_item.get("match_id"):
                    data.append(match_item)
        return data

    @staticmethod
    def get_actual_result(text):
        map_ = {"exp": "", "result": -1}
        int_list = []
        exp = re.compile("\\d+:\\d+")
        items = exp.findall(text)
        if len(items) > 0:
            map_["exp"] = items[0]
            exp = re.compile("\\d+")
            nums = exp.findall(items[0])
            for num in nums:
                int_list.append(int(num))
        if len(int_list) == 2:
            result = int_list[0] - int_list[1]
            if result > 0:
                map_["result"] = 3
            elif result < 0:
                map_["result"] = 0
            elif result == 0:
                map_["result"] = 1
        return map_

    @staticmethod
    def parse(matchs_data):
        print(matchs_data)
        MatchAnalyzeThread.batch_download_data_pages(matchs_data)
        for row in matchs_data:
            MatchAnalyzeThread.parse_odds(row, Helper.cache_file_name(
                "http://odds.500.com/fenxi/ouzhi-%i" % row["match_id"]))
            MatchAnalyzeThread.parse_baseface(row, Helper.cache_file_name(
                "http://odds.500.com/fenxi/shuju-%i" % row["match_id"]))
            MatchAnalyzeThread.detect_result(row)
            print("分析比赛", row["match_id"], "完成.")

        #remove formule object.
        for row in matchs_data:
            row.pop("formula_last_mid")
            row.pop("formula_total")
            row.pop("formula_last10")
            row.pop("formula_last6")
            row.pop("formula_last4")
            row["main_forces"] = list()
            row["client_forces"] = list()
            nums = Utils.parse_float_array(row["last_10_text_style"])
            if len(nums) > 3:
                row["main_forces"].append(nums[0])
                row["client_forces"].append(nums[2])
            nums = Utils.parse_float_array(row["last_6_text_style"])
            if len(nums) > 3:
                row["main_forces"].append(nums[0])
                row["client_forces"].append(nums[2])
            nums = Utils.parse_float_array(row["last_4_text_style"])
            if len(nums) > 3:
                row["main_forces"].append(nums[0])
                row["client_forces"].append(nums[2])
        print(matchs_data)
        if len(matchs_data) > 0:
            file_name = "cache_web_pages/%s.json" % matchs_data[0]["season_no"]
            Utils.text_write(file_name, [json.dumps(matchs_data)])
            if MatchAnalyzeThread.IS_HISTORY:
                MatchAnalyzeThread.save_history_data(matchs_data)

    #history data save
    @staticmethod
    def exclude_evt_(name):
        if name.find("超")!=-1 or name.find("甲")!=-1 or name.find("乙")!=-1:
            return False
        if name.find("英冠")!=-1:
            return False
        if name.find("日职")!=-1:
            return False
        return True

    @staticmethod
    def save_history_data(dataset):
        q = SessionFactory.new()
        rows = list()
        for row in dataset:
            if MatchAnalyzeThread.exclude_evt_(row.get("season_name")):
                continue
            b = Battle()
            b.actual_result = row.get("actual_result")
            b.balls_diff = row.get("ball_diff")
            b.detect_result = row.get("detect_result")
            b.evt_name = row.get("season_name")
            b.last_mix = row.get("last_mix_total_10")
            b.last_10 = row.get("last_10_text_style")
            b.last_6 = row.get("last_6_text_style")
            b.last_4 = row.get("last_4_text_style")
            b.last_battle = row.get("last_4_status_text_style")
            b.last_mix_battle = row.get("mix_310")
            b.score = row.get("score")
            b.url_key = row.get("match_id")
            b.vs_date = row.get("match_date")
            b.vs_team = row.get("team_names")
            MatchAnalyzeThread.odds_change_for_db("WL",row.get("Odds_WL"),row.get("Odds_WL_Change"),b)
            MatchAnalyzeThread.odds_change_for_db("LB",row.get("Odds_LB"),row.get("Odds_LB_Change"),b)
            MatchAnalyzeThread.odds_change_for_db("YB",row.get("Odds_YSB"),row.get("Odds_YSB_Change"),b)
            MatchAnalyzeThread.odds_change_for_db("BT",row.get("Odds_365"),row.get("Odds_365_Change"),b)
            MatchAnalyzeThread.odds_change_for_db("AM",row.get("Odds_AM"),row.get("Odds_AM_Change"),b)
            #other last5 com
            MatchAnalyzeThread.odds_change_for_db("Inerwetten",row.get("Odds_Inerwetten"),row.get("Odds_Inerwetten_Change"),b)
            MatchAnalyzeThread.odds_change_for_db("HG",row.get("Odds_HG"),row.get("Odds_HG_Change"),b)
            MatchAnalyzeThread.odds_change_for_db("WD",row.get("Odds_WD"),row.get("Odds_WD_Change"),b)
            MatchAnalyzeThread.odds_change_for_db("Bwin",row.get("Odds_Bwin"),row.get("Odds_Bwin_Change"),b)
            MatchAnalyzeThread.odds_change_for_db("10bet",row.get("Odds_10bet"),row.get("Odds_10bet_Change"),b)
            rows.append(b)
        q.add_all(rows)
        q.commit()

    @staticmethod
    def odds_change_for_db(com_name,odds,odds_c,parent):
        if len(odds) == 3:
            o = Odds()
            o.com_name = com_name
            o.r_3 = odds[0]
            o.r_1 = odds[1]
            o.r_0 = odds[2]
            if len(odds_c) == 3:
                o.r_3_c =  odds_c[0]
                o.r_1_c =  odds_c[1]
                o.r_0_c =  odds_c[2]
            parent.oddss.append(o)
        return None

    @staticmethod
    def detect_result(match):
        match["formula_total"].to_results()
        match["formula_last10"].to_results()
        match["formula_last6"].to_results()
        match["formula_last4"].to_results()
        avg_balls = (match["formula_total"].avg_balls + match["formula_last10"].avg_balls + match[
            "formula_last6"].avg_balls + match[
                         "formula_last4"].avg_balls) / 4
        num = round(avg_balls, 2)
        #scores += match["formula_last_mid"].to_results()
        #r = Result(scores,match["odds"])
        #match["result"]=r.detect(match["formula_last4"])
        diff = abs(num)
        match["ball_diff"] = num
        if 0 <= diff <= 0.5:
            if num > 0:
                match["detect_result"] = "13"
            else:
                match["detect_result"] = "10"
        if 0.5 < diff < 1.0:
            if num > 0:
                match["detect_result"] = "31"
            else:
                match["detect_result"] = "01"
        elif diff >= 1.0:
            if num > 0:
                match["detect_result"] = "3"
            else:
                match["detect_result"] = "0"

    @staticmethod
    def parse_baseface(row, f_name):
        row["last_mix_total_10"] = ""
        row["last_10_text_style"] = ""
        row["last_6_text_style"] = ""
        row["last_4_text_style"] = ""
        row["last_4_status_text_style"] = ""

        #预测赛果之用
        row["formula_total"] = Formula(Formula.TYPE_TOTAL)
        row["formula_last10"] = Formula(Formula.TYPE_LAST10)
        row["formula_last6"] = Formula(Formula.TYPE_LAST6)
        row["formula_last4"] = Formula(Formula.TYPE_LAST4)
        row["formula_last_mid"] = Formula(Formula.TYPE_LAST_MID)

        parser = Helper.soup(f_name)
        if not parser:
            return
        row["match_date"] = MatchAnalyzeThread.parse_match_date(parser)
        row["mix_310"] = MatchAnalyzeThread.parse_mix_battles(parser)
        ########################进球数比较引擎数据构造块#######################

        #球队主客混合平均进球数
        avg_balls = MatchAnalyzeThread.parse_balls_io_total_10(parser)
        if len(avg_balls) == 4:
            defence_main = Helper.zero_div(avg_balls[0], avg_balls[1])
            defence_client = Helper.zero_div(avg_balls[2], avg_balls[3])

            #本赛季
            row["formula_total"].main_force = avg_balls[0]
            row["formula_total"].client_force = avg_balls[2]
            row["formula_total"].main_defence = defence_main
            row["formula_total"].client_defence = defence_client

            win = "%.1f,%.1f" % (avg_balls[0], defence_main)
            lost = "%.1f,%.1f" % (avg_balls[2], defence_client)
            row["last_mix_total_10"] = "(%s)/(%s)" % (win, lost)

        #分主客区段平均进球数
        main_data = MatchAnalyzeThread.count_team_battle_balls_io("team_zhanji2_1", parser)
        client_data = MatchAnalyzeThread.count_team_battle_balls_io("team_zhanji2_0", parser)

        #视图数据
        row["last_4_status_text_style"] = "(%s)/(%s)" % ("".join(main_data["status"]), "".join(client_data["status"]))
        row["last_10_text_style"] = "(%.1f,%.1f)/(%.1f,%.1f)" % (
            main_data["last_10"]["win"], main_data["last_10"]["percentage"], client_data["last_10"]["win"],
            client_data["last_10"]["percentage"])
        row["last_6_text_style"] = "(%.1f,%.1f)/(%.1f,%.1f)" % (
            main_data["last_6"]["win"], main_data["last_6"]["percentage"], client_data["last_6"]["win"],
            client_data["last_6"]["percentage"])
        row["last_4_text_style"] = "(%.1f,%.1f)/(%.1f,%.1f)" % (
            main_data["last_4"]["win"], main_data["last_4"]["percentage"], client_data["last_4"]["win"],
            client_data["last_4"]["percentage"])

        #区段比较数据
        for last_n in [10, 6, 4]:
            formula_key = "formula_last%i" % last_n
            data_key = "last_%i" % last_n
            row[formula_key].main_force = main_data[data_key]["win"]
            row[formula_key].main_defence = main_data[data_key]["percentage"]
            row[formula_key].client_force = client_data[data_key]["win"]
            row[formula_key].client_defence = client_data[data_key]["percentage"]
            pass
            #掐头去尾中间比较数据
            # row["formula_last_mid"].main_force = main_data["last_mid"]["win"]
            # row["formula_last_mid"].main_defence = main_data["last_mid"]["percentage"]
            # row["formula_last_mid"].client_force = client_data["last_mid"]["win"]
            # row["formula_last_mid"].client_defence = client_data["last_mid"]["percentage"]
            ########################结束##########################################

    @staticmethod
    def parse_balls_io_total_10(parser):
        if not parser:
            return []
        div = parser.find("div", id="team_zhanji_1")
        io_balls = []
        if div:
            txt = div.get_text()
            io_balls = MatchAnalyzeThread.parse_balls_io(txt)
        div = parser.find("div", id="team_zhanji_0")
        if div:
            txt = div.get_text()
            io_balls += MatchAnalyzeThread.parse_balls_io(txt)
        return [(i / 10) for i in io_balls]

    @staticmethod
    def parse_balls_io(text):
        p = re.compile("进\\d+球失\\d+球", re.M)
        items = p.findall(text)
        if len(items) > 0:
            item = items[0]
            return Utils.parse_int_array(item)
        return []

        #分段计算平均进球数

    @staticmethod
    def count_team_avgballs_section(balls_arr, win_avg, lost_avg):
        avg = dict()
        size = len(balls_arr)
        win = 0.0
        lost = 0.0
        for b in balls_arr:
            w = b["win"]
            l = b["lost"]

            if l == 0 and w > 0:
                lost -= 0.5
            if w == l and w > 0:
                win += 0.5
                lost -= 1

            if Helper.zero_div(w, win_avg) >= 1.5:
                win += win_avg * 1.5
            else:
                win += w
            if Helper.zero_div(l, lost_avg) >= 1.5:
                lost += lost_avg * 1.5
            else:
                lost += l

        if lost <= 0:
            lost = 0.1

        if size != 0:
            win /= size
            lost /= size

        avg["win"] = round(win, 1) #平均进球数
        avg["lost"] = round(lost, 1) #平均丢球数
        avg["percentage"] = round(Helper.zero_div(win, lost), 1) #进失球比率
        return avg

    @staticmethod
    def count_team_battle_balls_io(div_id, parser):
        r = dict()
        is_main_team = True
        if div_id == "team_zhanji2_0":
            is_main_team = False
            #主/客场最近10场对战数据
        total_10_balls_io = MatchAnalyzeThread.parse_team_battle_balls_io_nums(div_id, parser, is_main_team)
        r["status"] = "".join(total_10_balls_io["310"])
        #主/客平均进球数
        win_avg = Helper.zero_div(sum([balls["win"] for balls in total_10_balls_io["scores"]]), 10)
        #主/客平均丢球数
        lost_avg = Helper.zero_div(sum([balls["lost"] for balls in total_10_balls_io["scores"]]), 10)

        r["last_10"] = MatchAnalyzeThread.count_team_avgballs_section(total_10_balls_io["scores"], win_avg, lost_avg)
        r["last_6"] = MatchAnalyzeThread.count_team_avgballs_section(total_10_balls_io["scores"][0:6], win_avg,
                                                                     lost_avg)
        r["last_4"] = MatchAnalyzeThread.count_team_avgballs_section(total_10_balls_io["scores"][0:4], win_avg,
                                                                     lost_avg)

        #掐头去尾
        copy = total_10_balls_io["scores"][:]
        mid_win = [w["win"] for w in copy]
        mid_lost = [w["lost"] for w in copy]
        mid_win.sort()
        mid_lost.sort()
        avg = {"win": 0.0, "lost": 0.0, "percentage": 0.0}
        if len(mid_win) > 3:
            avg["win"] = sum(mid_win[1:-1]) / (len(mid_win) - 2)
        if len(mid_lost) > 3:
            avg["lost"] = sum(mid_lost[1:-1]) / (len(mid_lost) - 2)
        avg["percentage"] = Helper.zero_div(avg["win"], avg["lost"])
        r["last_mid"] = avg
        return r

    @staticmethod
    def get_status_num_style(src):
        if src.find("h_red.png") != -1:
            return "3"
        elif src.find("m_green.png") != -1:
            return "1"
        elif src.find("l_blue.png") != -1:
            return "0"
        return ""

    @staticmethod
    def parse_mix_battles(base_face_parser):
        main = list()
        client = list()
        main_panel = base_face_parser.find("div", id="team_zhanji_1")
        if main_panel:
            imgs1 = main_panel.find_all("img")
            for img in imgs1:
                main.append(MatchAnalyzeThread.get_status_num_style(img["src"]))
        client_panel = base_face_parser.find("div", id="team_zhanji_0")
        if client_panel:
            imgs2 = client_panel.find_all("img")
            for img in imgs2:
                client.append(MatchAnalyzeThread.get_status_num_style(img["src"]))
        return "(%s)/(%s)" % ("".join(main[0:6]),"".join(client[0:6]))

    @staticmethod
    def parse_team_battle_balls_io_nums(div_id, parser, is_main=True):
        r = dict()
        r["310"] = list()
        scores = list()
        history_battle_data_panel = parser.find("div", id=div_id)
        if history_battle_data_panel:
            imgs = history_battle_data_panel.find_all("img")[0:6]
            for img in imgs:
                r["310"].append(MatchAnalyzeThread.get_status_num_style(img["src"]))
            aList = history_battle_data_panel.find_all("a")
            results = MatchAnalyzeThread.parse_history_battle_links(aList, 10)
            for score in results:
                if len(score) == 2:
                    s = dict()
                    if is_main:
                        s["win"] = score[0]
                        s["lost"] = score[1]
                    else:
                        s["win"] = score[1]
                        s["lost"] = score[0]
                    scores.append(s)
                    pass
                pass
        r["scores"] = scores
        return r

        #解析根据Limit数限定的历史战绩比分集合(N:M,..)

    @staticmethod
    def parse_history_battle_links(links, limit=10):
        items = []
        count = 0;
        for a in links:
            if a["href"].find("shuju-") != -1:
                if count == limit:
                    break
                nums = MatchAnalyzeThread.parse_history_score(a.get_text())
                items.append(nums)
                count += 1
        return items

    #解析单个历史战绩比分 N:M
    @staticmethod
    def parse_history_score(text):
        p = re.compile("\\d{1,2}:\\d{1,2}", re.M)
        items = p.findall(text)
        if len(items) > 0:
            r = items[0]
            return Utils.parse_int_array(r)
        return list()

    @staticmethod
    def parse_odds(row, f_name):
        row["Odds_WL"] = ""
        row["Odds_AM"] = ""
        row["Odds_LB"] = ""
        row["Odds_365"] = ""
        row["Odds_YSB"] = ""
        row["Odds_Inerwetten"] = ""#"Inerwetten"
        row["Odds_HG"] = ""#皇冠
        row["Odds_WD"] = ""#韦德
        row["Odds_Bwin"] = ""#Bwin
        row["Odds_10bet"] = ""#10bet

        row["Odds_WL_Change"] = ""
        row["Odds_AM_Change"] = ""
        row["Odds_LB_Change"] = ""
        row["Odds_365_Change"] = ""
        row["Odds_YSB_Change"] = ""
        row["Odds_Inerwetten_Change"] = ""#"Inerwetten"
        row["Odds_HG_Change"] = ""#皇冠
        row["Odds_WD_Change"] = ""#韦德
        row["Odds_Bwin_Change"] = ""#Bwin
        row["Odds_10bet_Change"] = ""#10bet

        parser = Helper.soup(f_name)
        if not parser:
            return

        #获取各大菠菜公司的初盘
        tr_ids = ["293", "5", "2", "3", "9", "4", "280", "6", "11", "16"]
        for tr_id in tr_ids:
            tr = parser.find("tr", id="tr_" + tr_id)
            if tr:
                nums = Utils.parse_float_array(tr.get_text())
                #nums = ["%.2f" % num for num in nums]
                if len(nums) > 3:
                    if tr_id == "293":
                        row["Odds_WL"] = nums[0:3]
                    elif tr_id == "5":
                        row["Odds_AM"] = nums[0:3]
                    elif tr_id == "2":
                        row["Odds_LB"] = nums[0:3]
                    elif tr_id == "3":
                        row["Odds_365"] = nums[0:3]
                    elif tr_id == "9":
                        row["Odds_YSB"] = nums[0:3]
                    elif tr_id == "4":#other
                        row["Odds_Inerwetten"] = nums[0:3]
                    elif tr_id == "280":
                        row["Odds_HG"] = nums[0:3]
                    elif tr_id == "6":
                        row["Odds_WD"] = nums[0:3]
                    elif tr_id == "11":
                        row["Odds_Bwin"] = nums[0:3]
                    elif tr_id == "16":
                        row["Odds_10bet"] = nums[0:3]

            tr = parser.find("tr", id="tr2_" + tr_id)
            if tr:
                nums = Utils.parse_float_array(tr.get_text())
                #nums = ["%.2f" % num for num in nums]
                if len(nums) > 3:
                    if tr_id == "293":
                        row["Odds_WL_Change"] = nums[0:3]
                    elif tr_id == "5":
                        row["Odds_AM_Change"] = nums[0:3]
                    elif tr_id == "2":
                        row["Odds_LB_Change"] = nums[0:3]
                    elif tr_id == "3":
                        row["Odds_365_Change"] = nums[0:3]
                    elif tr_id == "9":
                        row["Odds_YSB_Change"] = nums[0:3]
                    elif tr_id == "4":#other
                        row["Odds_Inerwetten_Change"] = nums[0:3]
                    elif tr_id == "280":
                        row["Odds_HG_Change"] = nums[0:3]
                    elif tr_id == "6":
                        row["Odds_WD_Change"] = nums[0:3]
                    elif tr_id == "11":
                        row["Odds_Bwin_Change"] = nums[0:3]
                    elif tr_id == "16":
                        row["Odds_10bet_Change"] = nums[0:3]

    @staticmethod
    def parse_match_date(parser):
        div = parser.find("div", class_="against_m")
        if div:
            txt = div.get_text();
            p1 = "\\d{4}-\\d{2}-\\d{2}"
            p2 = "\\d{2}:\\d{2}"
            r1 = re.compile(p1)
            r2 = re.compile(p2)
            items = r1.findall(txt) + r2.findall(txt)
            return " ".join(items)
        return ""

    @staticmethod
    def batch_download_data_pages(data):
        targetUrls = list()
        for item in data:
            targetUrls.append("http://odds.500.com/fenxi/shuju-%i" % item["match_id"])
            targetUrls.append("http://odds.500.com/fenxi/ouzhi-%i" % item["match_id"])
        random.shuffle(targetUrls)
        with ThreadPoolExecutor(max_workers=5) as executor:
            for url in targetUrls:
                f = Helper.cache_file_name(url)
                if os.path.exists(f):
                    continue
                executor.submit(Helper.web_page_download, url)
            executor.shutdown()


class Helper():
    @staticmethod
    def web_page_download(url, cached=True):
        while True:
            try:
                f = Helper.cache_file_name(url)
                if os.path.exists(f):
                    break
                else:
                    web_page = urllib.request.urlopen(url, timeout=15)
                    html = web_page.read()
                    html = html.decode('gb18030')
                    if cached:
                        local_file = Helper.cache_file_name(url)
                        Utils.text_write(local_file, [html])
                break
            except urllib.error.URLError as ex:
                info = sys.exc_info()
                print(info[0], ":", info[1], ex)
                continue
        print("%s have downloaded" % url)

    @staticmethod
    def soup(uri, local=True):
        soup = None
        if local:
            if os.path.exists(uri):
                html = Utils.text_read(uri)
                soup = BeautifulSoup(html)
        else:
            while True:
                try:
                    web_page = urllib.request.urlopen(uri, timeout=15)
                    html = web_page.read()
                    html = html.decode('gb18030')
                    soup = BeautifulSoup(html)
                    break
                except urllib.error.URLError as ex:
                    info = sys.exc_info()
                    print(info[0], ":", info[1], ex)
                    continue
        return soup

    @staticmethod
    def url_with_params(url):
        r1 = urllib.parse.urlsplit(str(url))
        if r1.query != "":
            return True
        return False

    @staticmethod
    def zero_div(a, b, extra=0.01):
        try:
            r = a / b
        except ZeroDivisionError:
            r = a / (b + extra)
        return round(r, 2)

    @staticmethod
    def cache_file_name(url):
        return "cache_web_pages/%s" % Utils.md5(url)

        # data = MatchAnalyzeThread.extract_matchs(["http://live.500.com/zucai.php?e=13100"])
        # MatchAnalyzeThread.parse(data)
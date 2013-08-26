__author__ = 'tinyms'
from lottery.parse import Helper, MatchAnalyzeThread
from tinyms.orm import SessionFactory


def last_days():
    expects = "http://www.500.com/pages/info/zhongjiang/index.php"
    soup = Helper.soup(expects, False)
    urls = list()
    if soup:
        select_box = soup.find("select", id="expect")
        opts = select_box.find_all("option")
        for opt in opts:
            urls.append("http://live.500.com/zucai.php?e=%s" % opt.get_text())
    return urls


def last_days2():
    urls = set()
    for year in [13, 12, 11]:
        for month in range(11):
            if year == 13 and month + 1 > 7:
                continue
            for expect in range(34):
                if year == 13 and expect + 1 > 7:
                    continue
                no = "%i%s%s" % (year, "{:0>2d}".format(month + 1), "{:0>2d}".format(expect + 1))
                urls.add("http://trade.500.com/bjdc/?expect=%s" % no)
    return urls


from sqlalchemy import create_engine

e = create_engine("sqlite+pysqlite:///matchs", echo=True)
SessionFactory.__engine__ = e
SessionFactory.create_tables()

urls = last_days2()
MatchAnalyzeThread.IS_HISTORY = True
thread = MatchAnalyzeThread()
thread.urls = urls
thread.start()
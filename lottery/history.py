__author__ = 'tinyms'
from lottery.parse import Helper,MatchAnalyzeThread
from lottery.entity import Battle,Odds
from tinyms.orm import SessionFactory

def last_days():
    expects = "http://www.500.com/pages/info/zhongjiang/index.php"
    soup = Helper.soup(expects,False)
    urls = list()
    if soup:
        select_box = soup.find("select",id="expect")
        opts = select_box.find_all("option")
        for opt in opts:
            urls.append("http://live.500.com/zucai.php?e=%s" % opt.get_text())
    return urls


from sqlalchemy import create_engine
e = create_engine("sqlite+pysqlite:///matchs", echo=True)
SessionFactory.__engine__ = e
SessionFactory.create_tables()

urls = last_days()
MatchAnalyzeThread.IS_HISTORY = True
thread = MatchAnalyzeThread()
thread.urls = urls
thread.start()

# q = SessionFactory().new()
#
# b = Battle()
# b.vs_team = "Test"
#
# o = Odds()
# o.com_name = "WL"
#
# b.oddss.append(o)
#
# q.add(b)
# q.commit()
__author__ = 'tinyms'

from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text
from tinyms.core.orm import Simplify,Entity,many_to_one,SessionFactory

SessionFactory.table_name_prefix("lottery")

class Battle(Entity,Simplify):
    score = Column(String(10))
    actual_result = Column(Integer)
    detect_result = Column(String(3))
    balls_diff = Column(Numeric(2,2))
    vs_team = Column(String(100))
    last_mix = Column(String(60))
    last_10 = Column(String(60))
    last_6 = Column(String(60))
    last_4 = Column(String(60))
    last_mix_battle = Column(String(60))
    last_battle = Column(String(60))
    url_key = Column(String(10))
    vs_date = Column(String(20))
    evt_name = Column(String(20))
    #oddss list


@many_to_one("Battle")
class Odds(Entity,Simplify):
    com_name = Column(String(12))
    r_3 = Column(Numeric(2,2))
    r_1 = Column(Numeric(2,2))
    r_0 = Column(Numeric(2,2))
    r_3_c = Column(Numeric(2,2))
    r_1_c = Column(Numeric(2,2))
    r_0_c = Column(Numeric(2,2))
    #battle one

class Expect(Entity,Simplify):
    no = Column(Integer(),unique=True,nullable=False)

@many_to_one("Expect")
class Betting(Entity,Simplify):
    seq = Column(Integer(),nullable=False)
    select_ = Column(String(3),nullable=False)
    reason = Column(Text())
    fix = Column(Boolean)

from tinyms.core.web import IRequest
from tinyms.core.point import route

@route("/betting")
class BettingController(IRequest):
    def get(self, *args, **kwargs):
        cnn = SessionFactory.new()
        opt=dict()
        opt["expects"]=list()
        for e in cnn.query(Expect).order_by(Expect.id.desc()):
            opt["expects"].append((e.id,e.no))
        print(opt["expects"])
        return self.render("betting.html",opt=opt)
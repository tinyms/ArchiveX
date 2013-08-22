__author__ = 'tinyms'

from sqlalchemy import Column, Integer, String, Numeric
from tinyms.orm import Simplify,Entity,many_to_one

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
    com_name = Column(String(10))
    r_3 = Column(Numeric(2,2))
    r_1 = Column(Numeric(2,2))
    r_0 = Column(Numeric(2,2))
    r_3_c = Column(Numeric(2,2))
    r_1_c = Column(Numeric(2,2))
    r_0_c = Column(Numeric(2,2))
    #battle one

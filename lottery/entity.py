__author__ = 'tinyms'

from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text
from tinyms.core.orm import Simplify, Entity, many_to_one, SessionFactory

SessionFactory.table_name_prefix("lottery_")


class Battle(Entity, Simplify):
    score = Column(String(10))
    actual_result = Column(Integer)
    detect_result = Column(String(3))
    balls_diff = Column(Numeric(2, 2))
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
class Odds(Entity, Simplify):
    com_name = Column(String(12))
    r_3 = Column(Numeric(2, 2))
    r_1 = Column(Numeric(2, 2))
    r_0 = Column(Numeric(2, 2))
    r_3_c = Column(Numeric(2, 2))
    r_1_c = Column(Numeric(2, 2))
    r_0_c = Column(Numeric(2, 2))
    #battle one


class Expect(Entity, Simplify):
    no = Column(Integer(), unique=True, nullable=False)


@many_to_one("Expect")
class Betting(Entity, Simplify):
    seq = Column(Integer(), nullable=False)
    select_3_to_2 = Column(String(3), nullable=False)
    select_2_to_1 = Column(String(3))
    last_first_select_rate = Column(Numeric(2, 2))
    reason = Column(Text())
    fix = Column(Boolean)
__author__ = 'tinyms'
__export__ = ["CustomDatabase"]

from sqlalchemy import Column, Integer, String, Numeric
from tinyms.orm import Simplify,Entity,many_to_one,SessionFactory

from sqlalchemy import create_engine
from tinyms.point import IDatabase

class CustomDatabase(IDatabase):
    def name(self):
        return "ArchiveX"
    def user(self):
        return "postgres"
    def password(self):
        return "1"
    def orm_engine(self):
        return create_engine("sqlite+pysqlite:///matchs", echo=True)
        #return create_engine("postgresql+psycopg2://postgres:1@localhost/ArchiveX", echo=True)

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

SessionFactory.table_name_prefix("m310")

class Odds(Entity,Simplify):
    com_name = Column(String(10))
    r_3 = Column(Numeric(2,2))
    r_1 = Column(Numeric(2,2))
    r_0 = Column(Numeric(2,2))
    r_3_c = Column(Numeric(2,2))
    r_1_c = Column(Numeric(2,2))
    r_0_c = Column(Numeric(2,2))
    #battle one

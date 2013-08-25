__author__ = 'tinyms'
__export__ = ["CustomDatabase"]

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


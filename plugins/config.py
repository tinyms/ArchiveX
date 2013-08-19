__author__ = 'tinyms'

__export__ = ["CustomDatabase"]

from sqlalchemy import create_engine
from tinyms.point import IDatabase

class CustomDatabase(IDatabase):
    def name(self):
        return "postgres"
    def user(self):
        return "postgres"
    def password(self):
        return "1"
    def table_name_prefix(self):
        return "ax"
    def engine(self):
        return create_engine("postgresql+psycopg2://postgres:1@localhost/postgres", echo=True)
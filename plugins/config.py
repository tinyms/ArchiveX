__author__ = 'tinyms'

__export__ = ["DefaultWebConfig"]

from sqlalchemy import create_engine
from tinyms.core.point import IWebConfig


class DefaultWebConfig(IWebConfig):
    def get_database_driver(self):
        return create_engine("sqlite+pysqlite:///arch.data", echo=True)
        #return create_engine("postgresql+psycopg2://postgres:1@localhost/ArchiveX", echo=True)


__author__ = 'tinyms'

__export__ = ["CustomDatabase"]

from tinyms.point import IDatabase

class CustomDatabase(IDatabase):
    def name(self):
        return "tinyms"
    def user(self):
        return "postgres"
    def password(self):
        return "1"
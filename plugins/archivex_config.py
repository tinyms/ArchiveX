__author__ = 'tinyms'

__plugin__=['Test']
from tinyms.point import IWebConfig

class Test(IWebConfig):
    def hello(self,msg):
        print(msg)
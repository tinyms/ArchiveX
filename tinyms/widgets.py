__author__ = 'tinyms'

from tornado.web import UIModule
from tornado.util import import_object

class DataTableModule(UIModule):
    def render(self,name):
        print(import_object(name))
        return name
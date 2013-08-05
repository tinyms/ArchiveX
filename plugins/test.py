__author__ = 'tinyms'

__plugin__=['AjaxTest']

from tinyms.point import IAjax

class AjaxTest(IAjax):

    __export__=["abc"]

    def __init__(self):
        pass

    def client_javascript_object_name(self):
        return "test_AjaxTest"

    def abc(self,**dict):
        print(dict)
        pass
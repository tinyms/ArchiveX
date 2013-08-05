__author__ = 'tinyms'

__export__=['AjaxTest']

import json
from tinyms.point import IAjax

class AjaxTest(IAjax):

    __export__=["console"]

    def __init__(self):
        pass

    def client_javascript_object_name(self):
        return "test_AjaxTest"

    def console(self,**dict_):
        print(dict_)
        return json.dumps(dict_)
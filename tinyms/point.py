__author__ = 'tinyms'
import json
from tinyms.common import JsonEncoder
#for plugin to extends
class IWebConfig():
    def settings(self, ws_setting):
        """
        Append or modify tornado setting
        :param ws_setting: dict()
        :return:
        """
        return

    def url_mapping(self, url_patterns):
        """
        Tornado url mapping
        Append (r'/some/any',RequestHandlerClass)
        :param url_patterns: list()
        :return:
        """
        return


class IAjax():
    def request(self, tornado_httpreq):
        self.req = tornado_httpreq

    def client_javascript_object_name(self):
        return "client_javascript_object_name_not_assign"

    def json(self,obj):
        return json.dumps(obj,cls=JsonEncoder)


class IApi():
    def request(self, tornado_httpreq):
        self.req = tornado_httpreq
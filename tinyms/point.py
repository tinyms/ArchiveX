__author__ = 'tinyms'
import json
from tinyms.common import JsonEncoder
#for plugin to extends
class EmptyClass():pass

class ObjectPool():
    api = dict()
    ajax = dict()

class IDatabase():
    def name(self):
        return "postgres"
    def user(self):
        return "postgres"
    def password(self):
        return ""
    def orm_engine(self):
        return None

class IWebConfig():
    def settings(self, ws_setting):
        """
        Append or modify tornado setting
        :param ws_setting: dict()
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

def api(key):
    """
    api mapping.
    """
    def ref(cls):
        ObjectPool.api[key] = cls
        return cls

    return ref

def ajax(key):
    """
    ajax mapping.
    """
    def ref(cls):
        ObjectPool.ajax[key] = cls
        return cls

    return ref
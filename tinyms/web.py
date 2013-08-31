__author__ = 'tinyms'

import json
import logging as log
from tornado.web import RequestHandler
from tornado.util import import_object
from sqlalchemy import func
from tinyms.common import Plugin, JsonEncoder, Utils
from tinyms.point import EmptyClass, ObjectPool
from tinyms.orm import SessionFactory
from tinyms.widgets import DataTableModule


class IRequest(RequestHandler):
    __url_patterns__ = list()
    __key_account_id__ = "__key_account_id__"
    __key_account_points__ = "__key_account_points__"
    __key_account_summary__ = "__key_account_summary__"

    def security_check(self,points=set()):
        diff = points & self.get_current_account_points()
        if len(diff) > 0:
            return True
        return False

    def get_current_user(self):
        """
        account id, int
        :return:
        """
        id = self.get_secure_cookie(IRequest.__key_account_id__)
        if id:
            return int(id)
        return None

    def get_current_account_points(self):
        """
        account security points: set('key1','key2',..)
        :return:
        """
        data = self.get_secure_cookie(IRequest.__key_account_points__)
        if data:
            return json.loads(data)
        return set()

    def get_current_account_summary(self):
        """
        current account name,sex,post,org etc.
        :return:
        """
        data = self.get_secure_cookie(IRequest.__key_account_points__)
        if data:
            return json.loads(data)
        return None

    def wrap_bean(self, bean_obj, excude_keys=["id"]):
        """
        把参数值填充到对象对应属性中，针对ORM中的Entity
        :param obj:
        :param excude_keys:
        :return:
        """
        dict_ = dict()
        args = self.request.arguments
        for key in args:
            if excude_keys.count(key) != -1:
                continue
            dict_[key] = self.get_argument(key)
        bean_obj.dict(dict_)
        return bean_obj

    def wrap_params_to_dict(self):
        dict_ = dict()
        args = self.request.arguments
        for key in args:
            dict_[key] = self.get_argument(key)
        return dict_

    def wrap_params_to_obj(self):
        obj = EmptyClass()
        args = self.request.arguments
        for key in args:
            setattr(obj, key, self.get_argument(key))
        return obj


def route(pattern):
    """
    url mapping.
    """

    def ref_pattern(cls):
        IRequest.__url_patterns__.append((pattern, cls))
        return cls

    return ref_pattern


@route(r"/datatable/(.*)")
class DataTableHandler(IRequest):
    def post(self, id):
        self.list(id)

    def delete(self, id):
        meta = DataTableModule.__entity_mapping__.get(id)
        if not meta:
            self.set_status(403, "Error!")
        entity = import_object(meta["name"])
        entity_id = self.get_argument("id")
        pass

    def update(self, id):
        meta = DataTableModule.__entity_mapping__.get(id)
        if not meta:
            self.set_status(403, "Error!")
        entity = import_object(meta["name"])
        entity_id = self.get_argument("id")
        pass

    def list(self, id):
        meta = DataTableModule.__entity_mapping__.get(id)
        if not meta:
            self.set_status(403, "Error!")
        print(self.request.arguments)
        entity = import_object(meta["name"])
        self.datatable_display_cols = meta["cols"]
        self.set_header("Content-Type", "text/json;charset=utf-8")
        display_start = Utils.parse_int(self.get_argument("iDisplayStart"))
        display_length = Utils.parse_int(self.get_argument("iDisplayLength"))
        #cols_num = self.get_argument("iColumns")
        gloabal_search_value = self.get_argument("sSearch")
        query_params = self.parse_search_params("sSearch_")
        print(query_params)
        cnn = SessionFactory.new()
        #here place custom filter
        total_query = cnn.query(func.count(entity.id))
        ds_query = cnn.query(entity)
        custom_filter = DataTableModule.__filter_mapping__.get(meta["name"])
        if custom_filter:
            custom_filter_obj = custom_filter()
            if hasattr(custom_filter_obj, "filter"):
                custom_filter_obj.filter(total_query, ds_query, self)
        total = total_query.scalar()
        ds = ds_query.offset(display_start).limit(display_length)
        results = dict()
        results["sEcho"] = self.get_argument("sEcho")
        results["iTotalRecords"] = total
        results["iTotalDisplayRecords"] = total
        results["aaData"] = [item.dict() for item in ds]
        self.write(json.dumps(results, cls=JsonEncoder))

    def parse_search_params(self, prefix):
        params = dict()
        args = self.request.arguments
        size = len(self.datatable_display_cols)
        for key in args:
            if key.find(prefix) != -1:
                index = Utils.parse_int(key)
                if size <= index:
                    continue
                v = self.get_argument(key)
                if v:
                    params[self.datatable_display_cols[index]] = v
        if len(params.keys()) == 0:
            return None
        return params


@route(r"/api/(.*)/(.*)")
class ApiHandler(IRequest):
    def get(self, key, method_name):
        self.req(key, method_name)

    def post(self, key, method_name):
        self.req(key, method_name)

    def req(self, key, method_name):
        """
        Url: localhost/api/key/method
        :param key: example: com.tinyms.category.v2
        :return:

        example:
            @api("com.tinyms.category.v2")
            class ApiTest():
                def create():
                    prama1 = self.param("prama1");
                    req = self.request # IRequest

            client side:
            $.post("/api/com.tinyms.category.v2/create",params,func,"json");
        """
        self.set_header("Content-Type", "text/json;charset=utf-8")
        if not key:
            self.write("Key require.")
        else:
            cls = ObjectPool.api.get(key)
            if not cls:
                self.write("Object not found.")
            else:
                obj = cls()
                if hasattr(obj, method_name):
                    setattr(obj, "request", self)
                    setattr(obj, "__params__", self.wrap_params_to_dict())
                    setattr(obj, "param", lambda key: obj.__params__.get(key))
                    func = getattr(obj, method_name)
                    result = func()
                    self.write(json.dumps(result, cls=JsonEncoder))


@route(r"/ajax/(.*).js")
class AjaxHandler(IRequest):
    def get(self, key):
        self.set_header("Content-Type", "text/javascript;charset=utf-8")
        if not key:
            self.write("alert('Ajax key require.')")
        else:
            cls = ObjectPool.ajax.get(key)
            if not cls:
                self.write("alert('Object not found.')")
            else:
                obj = cls()
                if hasattr(obj, "__export__") and type(obj.__export__) == list:
                    return self.render("core/ajax.tpl",
                                              module_name=obj.__class__.__module__,
                                              class_name=obj.__class__.__qualname__,
                                              key=key,
                                              methods=obj.__export__)
                else:
                    self.write("alert('Attr `__export__` not exists or blank!');")

    def post(self, key):

        data_type = self.get_argument("__data_type__")
        if data_type == "json":
            self.set_header("Content-Type", "text/json;charset=utf-8")
        elif data_type == "script":
            self.set_header("Content-Type", "text/javascript;charset=utf-8")
        elif data_type == "html":
            self.set_header("Content-Type", "text/html;charset=utf-8")

        if not key:
            self.write("alert('Ajax key require.')")
        else:
            cls = ObjectPool.ajax.get(key)
            if not cls:
                self.write("Class not found.")
            else:
                method_name = self.get_argument("__method_name__")
                obj = cls()
                if hasattr(obj, method_name):
                    setattr(obj, "request", self)
                    setattr(obj, "__params__", self.wrap_params_to_dict())
                    setattr(obj, "param", lambda key: obj.__params__.get(key))
                    func = getattr(obj, method_name)
                    result = func()
                    if data_type == "json":
                        self.write(json.dumps(result, cls=JsonEncoder))
                    else:
                        self.write(result)
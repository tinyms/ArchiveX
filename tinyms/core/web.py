__author__ = 'tinyms'

import json
from tornado.web import RequestHandler
from tinyms.core.common import JsonEncoder
from tinyms.core.point import EmptyClass, ObjectPool, route

class IRequest(RequestHandler):
    __key_account_id__ = "__key_account_id__"
    __key_account_points__ = "__key_account_points__"
    __key_account_summary__ = "__key_account_summary__"

    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)
        if not self.get_current_user():
            uri = self.request.uri
            security_urls = ObjectPool.security_filter_uri
            ignore = True
            for url in security_urls:
                if uri.startswith(url):
                    ignore = False
            if not ignore:
                self.redirect(self.get_login_url())

    def auth(self, points=set()):
        """
        细微控制数据输出,不产生页面跳转相关动作
        :param points:
        :return:
        """
        diff = points & self.get_current_account_points()
        if len(diff) > 0:
            return True
        return False

    def get_login_url(self):
        self.redirect("/login")

    def write_error(self, status_code, **kwargs):
        if status_code == 401:
            self.render("login.html")
        elif status_code == 403:
            self.render("err.html", reason="访问禁止")
        else:
            self.render("err.html", reason="服务器内部错误")

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

    def wrap_entity(self, entity_object, excude_keys=["id"]):
        """
        把参数值填充到对象对应属性中，针对ORM中的Entity
        :param obj:
        :param excude_keys:
        :return:
        """
        dict_ = dict()
        args = self.request.arguments
        for key in args.keys():
            if excude_keys.count(key) != 0:
                continue
            dict_[key] = self.get_argument(key)
        entity_object.dict(dict_)
        return entity_object

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
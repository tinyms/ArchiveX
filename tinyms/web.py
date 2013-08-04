__author__ = 'tinyms'

from tornado.web import RequestHandler
from tinyms.common import Plugin
from tinyms.point import IAjax,IApi

class ApiHandler(RequestHandler):

    def get(self,class_full_name,method_name):
        self.req(class_full_name,method_name)

    def post(self,class_full_name,method_name):
        self.req(class_full_name,method_name)

    def req(self,class_full_name,method_name):
        """
        Url: localhost/api/module.class/method
        :param class_full_name:
        :return:
        """
        ver = self.get_argument("ver");
        self.set_header("Content-Type","text/json;charset=utf-8")
        if not class_full_name:
            return
        obj = Plugin.get(IApi,class_full_name)
        if not obj:
            return
        if hasattr(obj,method_name):
            func = obj.__getattribute__(method_name)
            argcount = func.__code__.co_argcount
            params_name = func.__code__.co_varnames[1:argcount]
        pass

class AjaxHandler(RequestHandler):

    def get(self,class_full_name):
        self.set_header("Content-Type","text/javascript;charset=utf-8")
        if not class_full_name:
            return
        obj = Plugin.get(IAjax,class_full_name)
        if not obj:
            return
        if hasattr(obj,"__export__"):
            if len(obj.__export__) > 0:
                client_js_object_name = obj.client_javascript_object_name()
                js_ = """
                    %s.%s=function(%s,func){
                        var params_ = %s;
                        params_.server_side_func_name = "%s";
                        $.post("/ajax/%s.js",params_,function(data){func(data);},"json");
                    };
                """
                js_buffer = list()
                js_buffer.append("var %s = {};" % client_js_object_name)
                for export_func in obj.__export__:
                    func = obj.__getattribute__(export_func)
                    argcount = func.__code__.co_argcount
                    if argcount < 2:
                        continue
                    params_name = func.__code__.co_varnames[1:argcount-1]
                    js_params_pass = list()
                    for param_name in params_name:
                        js_params_pass.append("%s:%s" % (param_name,param_name))
                    js_buffer.append(js_ % (client_js_object_name,export_func,",".join(params_name),"{%s}" % ",".join(js_params_pass),export_func,class_full_name))
                    self.write("".join(js_buffer))
        else:
            self.write("console.log('Attr `__export__` Not exist');")

    def post(self,class_full_name):
        self.set_header("Content-Type","text/json;charset=utf-8")
        if not class_full_name:
            return
        obj = Plugin.get(IAjax,class_full_name)
        if not obj:
            return
        func_name = self.get_argument("server_side_func_name")
        if hasattr(obj,func_name):
            func = obj.__getattribute__(func_name)
            argcount = func.__code__.co_argcount
            params_name = func.__code__.co_varnames[1:argcount]
        pass
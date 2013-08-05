__author__ = 'tinyms'

import json
from tornado.web import RequestHandler
from tinyms.common import Plugin
from tinyms.point import IAjax,IApi

class IRequest(RequestHandler):pass

class ApiHandler(IRequest):

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
            func_params = json.loads(self.get_argument("dict_params"))
            obj.request(self)
            result = func(**func_params)
            self.write(json.dumps(result))

class AjaxHandler(IRequest):

    def get(self,class_full_name):
        self.set_header("Content-Type","text/javascript;charset=utf-8")
        if not class_full_name:
            return
        obj = Plugin.get(IAjax,class_full_name)
        if not obj:
            return
        if hasattr(obj,"__export__"):
            if len(obj.__export__) > 0:
                if not hasattr(obj,"client_javascript_object_name"):
                    print("client javascript object name not assign.")
                    return
                client_js_object_name = obj.client_javascript_object_name()
                js_ = """
                    %s.%s=function(dict_params, func, data_type){
                        var p_ = {};
                        p_.__func_dict_params__ = JSON.stringify(dict_params);
                        p_.__func_name__ = "%s";
                        p_.__data_type__ = data_type;
                        var req = $.ajax({
                            url: "/ajax/%s.js",type:"POST",data:p_,dataType:data_type
                        });
                        req.done(function(data){func(true,data);});
                        req.fail(function(jqXHR, textStatus) {
                            alert( "Request failed: " + textStatus );
                            func(false,textStatus);
                        })
                    };
                """
                js_buffer = list()
                js_buffer.append("var %s = {};" % client_js_object_name)
                for export_func in obj.__export__:
                    js_buffer.append(js_ % (client_js_object_name,
                                            export_func,
                                            export_func,
                                            class_full_name))
                    self.write("".join(js_buffer))
        else:
            self.write("console.log('Attr `__export__` Not exist');")

    def post(self,class_full_name):
        func_return_data_type = self.get_argument("__data_type__")
        if func_return_data_type == "json":
            self.set_header("Content-Type","text/json;charset=utf-8")
        elif func_return_data_type == "script":
            self.set_header("Content-Type","text/javascript;charset=utf-8")
        elif func_return_data_type == "html":
            self.set_header("Content-Type","text/html;charset=utf-8")
        if not class_full_name:
            return
        obj = Plugin.get(IAjax,class_full_name)
        if not obj:
            return
        func_name = self.get_argument("__func_name__")
        func_params = json.loads(self.get_argument("__func_dict_params__"))
        if hasattr(obj,func_name):
            obj.request(self)
            func = obj.__getattribute__(func_name)
            result = func(**func_params)
            self.write(result)
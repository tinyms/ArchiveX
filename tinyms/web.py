__author__ = 'tinyms'

import json
import logging as log
from tornado.web import RequestHandler
from tornado.util import import_object
from sqlalchemy import func
from tinyms.common import Plugin,JsonEncoder,Utils
from tinyms.point import IAjax, IApi
from tinyms.orm import SessionFactory
from tinyms.widgets import DataTableModule



class IRequest(RequestHandler):
    __url_patterns__ = list()

def route(pattern):
    """
    url mapping.
    """
    def ref_pattern(cls):
        IRequest.__url_patterns__.append((pattern,cls))
        return cls

    return ref_pattern

@route(r"/datatable/(.*)")
class DataTableHandler(IRequest):
    def post(self, id):
        meta = DataTableModule.__entity_mapping__.get(id)
        if not meta:
            self.set_status(403,"Error!")
        print(self.request.arguments)
        entity = import_object(meta["name"])
        self.datatable_display_cols = meta["cols"]
        self.set_header("Content-Type", "text/json;charset=utf-8")
        display_start = Utils.parse_int(self.get_argument("iDisplayStart"))
        display_length = Utils.parse_int(self.get_argument("iDisplayLength"))
        cols_num = self.get_argument("iColumns")
        gloabal_search_value = self.get_argument("sSearch")
        query_params = self.parse_search_params("sSearch_")
        cnn = SessionFactory.new()
        nums = cnn.query(func.count(entity.id)).one()
        ds = cnn.query(entity).offset(display_start).limit(display_length)
        results = dict()
        results["sEcho"] = self.get_argument("sEcho")
        results["iTotalRecords"] = nums[0]
        results["iTotalDisplayRecords"] = nums[0]
        results["aaData"] = [item.dict() for item in ds]
        log.info(results)
        self.write(json.dumps(results,cls=JsonEncoder))

    def parse_search_params(self,prefix):
        params = dict()
        args = self.request.arguments
        size = len(self.datatable_display_cols)
        for key in args:
            if key.find(prefix)!=-1:
                index = Utils.parse_int(key)
                if size <= index:
                    continue
                params[self.datatable_display_cols[index]] = args[key]
        return params

@route(r"/api/(.*)/(.*)")
class ApiHandler(IRequest):
    def get(self, class_full_name, method_name):
        self.req(class_full_name, method_name)

    def post(self, class_full_name, method_name):
        self.req(class_full_name, method_name)

    def req(self, class_full_name, method_name):
        """
        Url: localhost/api/module.class/method
        :param class_full_name:
        :return:
        """
        #ver = self.get_argument("ver")
        self.set_header("Content-Type", "text/json;charset=utf-8")
        if not class_full_name:
            self.write("Class Name Require.")
        else:
            obj = Plugin.get(IApi, class_full_name)
            if not obj:
                self.write("Class Not Found.")
            else:
                if hasattr(obj, "__export__"):
                    if obj.__export__.count(method_name) > 0:
                        if hasattr(obj, method_name):
                            func = obj.__getattribute__(method_name)
                            func_params = json.loads(self.get_argument("params"))
                            obj.request(self)
                            result = func(**func_params)
                            self.write(json.dumps(result,cls=JsonEncoder))
                        else:
                            self.write("The method `%s` not found." % method_name)

@route(r"/ajax/(.*).js")
class AjaxHandler(IRequest):
    def get(self, class_full_name):
        self.set_header("Content-Type", "text/javascript;charset=utf-8")
        if not class_full_name:
            self.write("alert('Class Name Require.')")
        else:
            obj = Plugin.get(IAjax, class_full_name)
            if not obj:
                self.write("alert('Class Not Found.')")
            else:
                if hasattr(obj, "__export__"):
                    if len(obj.__export__) > 0:
                        if not hasattr(obj, "client_javascript_object_name"):
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

    def post(self, class_full_name):

        func_return_data_type = self.get_argument("__data_type__")
        if func_return_data_type == "json":
            self.set_header("Content-Type", "text/json;charset=utf-8")
        elif func_return_data_type == "script":
            self.set_header("Content-Type", "text/javascript;charset=utf-8")
        elif func_return_data_type == "html":
            self.set_header("Content-Type", "text/html;charset=utf-8")

        if not class_full_name:
            self.write("Class Name Require.")
        else:
            obj = Plugin.get(IAjax, class_full_name)
            if not obj:
                self.write("Class Not Found.")
            else:
                func_name = self.get_argument("__func_name__")
                func_params = json.loads(self.get_argument("__func_dict_params__"))
                if hasattr(obj, func_name):
                    obj.request(self)
                    func = obj.__getattribute__(func_name)
                    result = func(**func_params)
                    self.write(result)
__author__ = 'tinyms'

import json
from tornado.web import UIModule
from tornado.util import import_object
from tinyms.core.common import Utils
from tinyms.core.point import ui

class IWidget(UIModule):
    pass

def datatable_filter(entity_name):
    """
    custom datatable filter.自定义DataTable数据查询过滤，只要加上这个
    装饰器，并传入datatable对应的实体名，使用此装饰器的类必须实现一个filter的方法
    """
    def ref_pattern(cls):
        DataTableModule.__filter_mapping__[entity_name] = cls
        return cls

    return ref_pattern

@ui("DataTable")
class DataTableModule(IWidget):
    __filter_mapping__ = dict()
    __entity_mapping__ = dict()

    def render(self, **prop):
        self.dom_id = prop.get("id")#client dom id
        self.cols = prop.get("cols")#entity field list
        self.titles = prop.get("titles")#title list
        self.entity_full_name = prop.get("entity")#entity name
        self.form_id = prop.get("form_id")#Edit form
        self.search_field = prop.get("search_field")#default search field name

        self.col_title_mapping = dict()
        for i,col in enumerate(self.cols):
            self.col_title_mapping[col] = self.titles[i]

        if not self.form_id:
            self.form_id = ""
        if not self.entity_full_name:
            return "Require entity full name."
        self.datatable_key = Utils.md5(self.entity_full_name)

        sub = dict()
        sub["name"] = self.entity_full_name
        sub["cols"] = self.cols
        DataTableModule.__entity_mapping__[self.datatable_key] = sub

        tag = ""
        for title in self.titles:
            tag += "<th>" + title + "</th>"
        tag += "<th>#</th>"
        return self.render_string("widgets/datatable_html.tpl",domId=self.dom_id,thTags = tag)

    def html_body(self):
        data = dict()
        data["dom_id"] = self.dom_id
        data["use_sys_editform"] = False
        if not self.form_id:
            obj = import_object(self.entity_full_name)()
            metas = obj.cols_meta()
            col_defs = list()
            for col in self.cols:
                col_def = dict()
                col_def["name"]=col
                col_def["type"]=""
                col_def["required"]=""
                for meta in metas:
                    if meta["name"]==col:
                        if not meta["nullable"]:
                            col_def["required"]="required"
                        if meta["type"]=="int":
                            col_def["type"]="digits"
                        elif meta["type"]=="numeric":
                            col_def["type"]="number"
                        elif meta["type"]=="date":
                            col_def["type"]="date"
                col_defs.append(col_def)
            data["use_sys_editform"] = True
            data["col_title_mapping"] = self.col_title_mapping
            data["cols"]=col_defs
        return self.render_string("widgets/editform.tpl",opt=data)

    def embedded_javascript(self):
        params_ = dict()
        params_["id"] = self.dom_id
        params_["edit_form_id"] = self.form_id
        params_["entity_name"] = self.datatable_key

        html_col = list()
        filter_configs = list()

        index = 0
        for col in self.cols:
            filter_configs.append({"type": "text"})
            html_col.append({"mData": col, "sTitle": self.titles[index], "sDefaultContent": ""})
            index += 1

        params_["col_defs"] = json.dumps(html_col)
        params_["filter_configs"] = json.dumps(filter_configs)
        return self.render_string("widgets/datatable_script.tpl", opt=params_)

    def javascript_files(self):
        items = list();
        items.append("/static/jslib/datatable/js/jquery.dataTables.min.js")
        items.append("/static/jslib/datatable/js/jquery.dataTables.columnFilter.js")
        items.append("/static/jslib/datatable/extras/tabletools/js/ZeroClipboard.js")
        items.append("/static/jslib/datatable/extras/tabletools/js/TableTools.min.js")
        items.append("/static/jslib/tinyms.datatable.js")
        return items

    def css_files(self):
        items = list();
        items.append("/static/jslib/datatable/css/jquery.dataTables.css")
        items.append("/static/jslib/datatable/extras/tabletools/css/TableTools.css")
        return items
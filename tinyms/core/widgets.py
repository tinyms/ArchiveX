__author__ = 'tinyms'

import json
from tornado.web import UIModule

from tinyms.core.common import Utils
from tinyms.core.point import ObjectPool

class IWidget(UIModule):
    pass

def ui(name):
    """
    ui mapping. 配置UI至模版可用
    """
    def ref_pattern(cls):
        ObjectPool.ui_mapping[name] = cls
        return cls

    return ref_pattern

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

        html = """
         <table id="{0}"><tfoot><tr>{1}</tr></tfoot></table>
        """
        tag = ""
        for title in self.titles:
            tag += "<th>" + title + "</th>"
        tag += "<th>#</th>"
        return html.format(self.dom_id, tag)

    def html_body(self):
        data = dict()
        data["dom_id"] = self.dom_id
        data["use_sys_editform"] = False
        if not self.form_id:
            data["use_sys_editform"] = True
            data["col_title_mapping"] = self.col_title_mapping
            data["cols"]=self.cols
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
        return self.render_string("widgets/datatable.tpl", opt=params_)

    def javascript_files(self):
        items = list();
        items.append("/static/jslib/jquery-ui/js/jquery-ui-1.10.3.custom.min.js")
        items.append("/static/jslib/datatable/js/jquery.dataTables.min.js")
        items.append("/static/jslib/datatable/js/jquery.dataTables.columnFilter.js")
        items.append("/static/jslib/datatable/extras/tabletools/js/ZeroClipboard.js")
        items.append("/static/jslib/datatable/extras/tabletools/js/TableTools.min.js")
        items.append("/static/jslib/datatable/extras/fixedheader/FixedHeader.min.js")
        return items

    def css_files(self):
        items = list();
        items.append("/static/jslib/jquery-ui/css/smoothness/jquery-ui-1.10.3.custom.min.css")
        items.append("/static/jslib/datatable/css/jquery.dataTables.css")
        items.append("/static/jslib/datatable/extras/tabletools/css/TableTools.css")
        return items
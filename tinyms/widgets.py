__author__ = 'tinyms'

import json
from tornado.web import UIModule
from tinyms.common import Utils


class DataTableModule(UIModule):
    __entity_mapping__ = dict()

    def render(self, **prop):
        self.dom_id = prop.get("id")#client dom id
        self.cols = prop.get("cols")#entity field list
        self.titles = prop.get("titles")#title list
        self.entity_full_name = prop.get("entity")#entity name
        self.form_id = prop.get("form_id")#Edit form
        self.search_field = prop.get("search_field")#default search field name
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
        html = """
         <div id="{0}_EditFormDialog"></div>
        """
        return html.format(self.dom_id)

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
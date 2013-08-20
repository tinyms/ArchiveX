__author__ = 'tinyms'

import json
from tornado.web import UIModule
from tinyms.common import Utils

class DataTableModule(UIModule):
    __entity_mapping__ = dict()
    def render(self,**prop):
        self.dom_id = prop.get("id")
        self.cols = prop.get("cols")
        self.titles = prop.get("titles")
        self.entity_full_name =  prop.get("entity")
        if not self.entity_full_name:
            return "Require entity full name."
        self.params = prop.get("params")
        DataTableModule.__entity_mapping__[Utils.md5(self.entity_full_name)] = self.entity_full_name
        if not self.params:
            self.params = "DataTable_FNServerParams"
        html = """
         <table id="{0}"><thead><tr>{1}</tr></thead></table>
        """
        html_titles = ""
        for title in self.titles:
            html_titles += "<th>"+title+"</th>"
        #print(import_object(prop["entity_name"]))
        return html.format(self.dom_id,html_titles)
    def embedded_javascript(self):
        js = """
            function DataTable_FNServerParams(aoData){}
            $(document).ready(function(){
                var %s = $("#%s").dataTable({"bServerSide":true,
                "bProcessing":true,
                "asSorting":true,
                "sAjaxSource":"/datatable/%s",
                "sServerMethod":"POST",
                "fnServerParams":function(aoData){try{%s(aoData);}catch(e){}},
                "aoColumns":%s});
            });
        """
        html_col = list()
        for col in self.cols:
            html_col.append({"mData":col})

        return js % (self.dom_id,self.dom_id,Utils.md5(self.entity_full_name),self.params,json.dumps(html_col))
    def javascript_files(self):
        return "/static/jslib/datatable/js/jquery.dataTables.min.js"
    def css_files(self):
        return "/static/jslib/datatable/css/jquery.dataTables.css"
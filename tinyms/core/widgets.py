__author__ = 'tinyms'

import json
from tornado.web import UIModule
from tornado.util import import_object
from tinyms.core.common import Utils
from tinyms.core.point import ui, route
from tinyms.core.common import JsonEncoder
from tinyms.core.orm import SessionFactory
from tinyms.core.web import IRequest
from sqlalchemy import func


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
    __default_search_fields__ = dict()

    def render(self, **prop):
        self.dom_id = prop.get("id")#client dom id
        self.cols = prop.get("cols")#entity field list
        self.titles = prop.get("titles")#title list
        self.entity_full_name = prop.get("entity")#entity name
        self.form_id = prop.get("form")#Edit form id
        self.search_fields = prop.get("search_fields")#default search field name,and text type,

        if not self.form_id:
            self.form_id = ""
        if not self.entity_full_name:
            return "Require entity full name."
        self.datatable_key = Utils.md5(self.entity_full_name)
        if self.search_fields:
            DataTableModule.__default_search_fields__[self.datatable_key] = self.search_fields.split(",")
        else:
            DataTableModule.__default_search_fields__[self.datatable_key] = []
        sub = dict()
        sub["name"] = self.entity_full_name
        sub["cols"] = self.cols
        DataTableModule.__entity_mapping__[self.datatable_key] = sub

        tag = ""
        for title in self.titles:
            tag += "<th>" + title + "</th>"
        tag += "<th>#</th>"

        opt = dict()
        opt["id"] = self.dom_id
        opt["thTags"] = tag
        opt["entity_name_md5"] = self.datatable_key
        opt["edit_form_id"] = self.form_id
        form = self.create_editform()
        opt["use_sys_editform"] = form["use_sys_editform"]
        opt["cols"] = form.get("cols")
        html_col = list()

        index = 0
        for col in self.cols:
            html_col.append(
                {"mData": col, "sTitle": self.titles[index], "sClass": "datatable_column_" + col, "sDefaultContent": ""})
            index += 1

        opt["col_defs"] = json.dumps(html_col)
        return self.render_string("widgets/datatable_html.tpl", opt=opt)

    def create_editform(self):
        data = dict()
        data["dom_id"] = self.dom_id
        data["use_sys_editform"] = True
        if not self.form_id:
            obj = import_object(self.entity_full_name)()
            metas = obj.cols_meta()
            col_defs = list()
            for meta in metas:
                if meta["name"] == "id":
                    continue
                col_def = dict()
                col_def["name"] = meta["name"]
                col_def["type"] = ""
                col_def["required"] = ""
                if not meta["nullable"]:
                    col_def["required"] = "required"
                if meta["type"] == "int":
                    col_def["type"] = "digits"
                elif meta["type"] == "numeric":
                    col_def["type"] = "number"
                elif meta["type"] == "date":
                    col_def["type"] = "date"
                col_defs.append(col_def)
            data["use_sys_editform"] = True
            data["cols"] = col_defs
        else:
            data["use_sys_editform"] = False
        return data

    def javascript_files(self):
        items = list();
        items.append("/static/jslib/datatable/js/jquery.dataTables.1.9.4.modified.js")
        items.append("/static/jslib/datatable/extras/tabletools/js/ZeroClipboard.js")
        items.append("/static/jslib/datatable/extras/tabletools/js/TableTools.min.js")
        items.append("/static/jslib/tinyms.datatable.js")
        return items

    def css_files(self):
        items = list();
        items.append("/static/jslib/datatable/css/jquery.dataTables.css")
        items.append("/static/jslib/datatable/extras/tabletools/css/TableTools.css")
        return items


@route(r"/datatable/(.*)/(.*)")
class DataTableHandler(IRequest):
    def post(self, id, act):
        if act == "list":
            self.list(id)
        elif act == "save":
            self.update(id)
        elif act == "saveNext":
            self.update(id)
        elif act == "delete":
            self.delete(id)

    def delete(self, id):
        self.set_header("Content-Type", "text/json;charset=utf-8")
        meta = DataTableModule.__entity_mapping__.get(id)
        if not meta:
            self.set_status(403, "Error!")
        entity = import_object(meta["name"])
        message = dict()
        rec_id = self.get_argument("id")
        cnn = SessionFactory.new()
        cur_row = cnn.query(entity).get(rec_id)
        cnn.delete(cur_row)
        cnn.commit()
        message["success"] = True
        message["msg"] = "Deleted"
        self.write(json.dumps(message))

    def update(self, id):
        self.set_header("Content-Type", "text/json;charset=utf-8")
        meta = DataTableModule.__entity_mapping__.get(id)
        if not meta:
            self.set_status(403, "Error!")
        entity = import_object(meta["name"])
        message = dict()
        rec_id = self.get_argument("id")
        if not rec_id:
            obj = self.wrap_entity(entity())
            cnn = SessionFactory.new()
            cnn.add(obj)
            cnn.commit()
            message["success"] = True
            message["msg"] = "Newed"
            self.write(json.dumps(message))
        else:
            cnn = SessionFactory.new()
            cur_row = cnn.query(entity).get(rec_id)
            self.wrap_entity(cur_row)
            cnn.commit()
            message["success"] = True
            message["msg"] = "Updated"
            self.write(json.dumps(message))

    def list(self, id):
        meta = DataTableModule.__entity_mapping__.get(id)
        if not meta:
            self.set_status(403, "Error!")
        entity = import_object(meta["name"])
        self.datatable_display_cols = meta["cols"]
        self.set_header("Content-Type", "text/json;charset=utf-8")
        display_start = Utils.parse_int(self.get_argument("iDisplayStart"))
        display_length = Utils.parse_int(self.get_argument("iDisplayLength"))
        #cols_num = self.get_argument("iColumns")

        #全局搜索处理段落
        default_search_value = Utils.trim(self.get_argument("sSearch"))
        query_params = self.parse_search_params("sSearch_")
        default_search_fields = DataTableModule.__default_search_fields__.get(id)
        default_search_sqlwhere = ""
        default_search_sqlwhere_params = dict()
        if default_search_value and default_search_fields:
            temp_sql = list()
            for field_name in default_search_fields:
                temp_sql.append("%s like :%s" % (field_name, field_name))
                default_search_sqlwhere_params[field_name] = "%" + default_search_value + "%"
            default_search_sqlwhere = " OR ".join(temp_sql)

        #排序处理段落
        sort_params = self.parse_search_params("iSortCol_")
        sort_direct_params = self.parse_search_params("sSortDir_")
        order_sqlwhere = ""
        for k, v in sort_params.items():
            order_sqlwhere += "1=1 ORDER BY %s %s" % (k, sort_direct_params[k])
            break
            #DataGrid数据查询段落
        cnn = SessionFactory.new()
        #here place custom filter
        total_query = cnn.query(func.count(entity.id))
        ds_query = cnn.query(entity)
        custom_filter = DataTableModule.__filter_mapping__.get(meta["name"])
        if custom_filter:
            custom_filter_obj = custom_filter()
            if hasattr(custom_filter_obj, "filter"):
                total_query = custom_filter_obj.total_filter(total_query, query_params, self)
                ds_query = custom_filter_obj.dataset_filter(ds_query, query_params, self)
        if default_search_value:
            total_query = total_query.filter(default_search_sqlwhere).params(**default_search_sqlwhere_params)
            ds_query = ds_query.filter(default_search_sqlwhere).params(**default_search_sqlwhere_params)
        if order_sqlwhere:
            ds_query = ds_query.filter(order_sqlwhere)
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

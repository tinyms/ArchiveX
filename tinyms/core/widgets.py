__author__ = 'tinyms'

import json
from tornado.web import UIModule
from tornado.util import import_object
from tinyms.core.common import Utils, JsonEncoder
from tinyms.core.point import ui, route, ObjectPool, EmptyClass
from tinyms.core.orm import SessionFactory
from tinyms.core.web import IRequest
from sqlalchemy import func
from tinyms.dao.account import AccountHelper


class IWidget(UIModule):
    pass


@ui("Version")
class VersionModule(IWidget):
    def render(self, *args, **kwargs):
        return "&copy; ArchiveX 2013, v1.0"


@ui("CurrentAccountName")
class CurrentAccountName(IWidget):
    def render(self, account_id=None):
        return AccountHelper.name(account_id)


@ui("SideBar")
class SideBar(IWidget):
    archives_show = False
    role_org_show = False
    sys_params_show = False

    def render(self, account_id=None):
        if not account_id:
            return ""
        points = list(AccountHelper.points(account_id))
        if points.count("tinyms.sidebar.archives.show"):
            self.archives_show = True
        if points.count("tinyms.sidebar.role_org.show"):
            self.role_org_show = True
        if points.count("tinyms.sidebar.sys_params.show"):
            self.sys_params_show = True
        custom_menus = ObjectPool.sidebar_menus
        first_levels = list()
        for menu in custom_menus:
            if menu[1].count("/") == 1:
                first_levels.append(menu)
        html_builder = list()
        self.sort_menus(first_levels)
        for first in first_levels:
            if first[4] and points.count(first[4]) == 0:
                continue
            p = '<a href="' + first[2] + '"><i class="' + first[5] + ' icon-xlarge"></i><span>' + first[
                3] + '</span></a>'
            subs = self.children(first[1])
            if len(subs) > 0:
                html_builder.append('<li class="dropdown-submenu">')
                html_builder.append(p)
                html_builder.append('<ul class="dropdown-menu">')
                self.sort_menus(subs)
                for sub in subs:
                    if sub[4] and points.count(sub[4]) == 0:
                        continue
                    html_builder.append('<li><a href="' + sub[2] + '">' + sub[3] + '</a></li>')
                    pass
                html_builder.append('</ul>')
                html_builder.append('</li>')
            else:
                html_builder.append("<li>" + p + "</li>")
        menu_html = "".join(html_builder)
        context = dict()
        context["menu"] = menu_html
        context["archives_show"] = self.archives_show
        context["role_org_show"] = self.role_org_show
        context["sys_params_show"] = self.sys_params_show
        return self.render_string("workbench/sidebar.html", context=context)

    def children(self, path):
        subs = list()
        for menu in ObjectPool.sidebar_menus:
            if menu[1].startswith(path + "/"):
                subs.append(menu)
        return subs

    def sort_menus(self, items):
        items.sort(key=lambda x: x[0])


def datatable_filter(entity_name):
    """
    custom datatable filter.自定义DataTable数据查询过滤，只要加上这个
    装饰器，并传入datatable对应的实体名，使用此装饰器的类必须实现一个filter的方法
    """

    def ref_pattern(cls):
        DataTableModule.__filter_mapping__[entity_name] = cls
        return cls

    return ref_pattern


@ui("DataComboBox")
class DataComboBoxModule(IWidget):
    def render(self, **prop):
        self.dom_id = prop.get("id")
        self.cols = prop.get("cols")
        self.sort_sql = prop.get("sort_sql")
        self.entity_full_name = prop.get("entity")
        self.query_class = prop.get("query_class") # obj prop `data` func return [(k,v),(k,v)...]
        self.allow_blank_select = prop.get("allow_blank_select")
        html = list()
        html.append("<select id='%s' name='%s' class='form-control'>" % (self.dom_id, self.dom_id))
        if self.allow_blank_select:
            html.append("<option value=''> </option>")
        if not self.query_class:
            if not self.entity_full_name:
                return "<small>Require entity full name.</small>"
            if self.entity_full_name:
                cls = import_object(self.entity_full_name)
                cnn = SessionFactory.new()
                q = cnn.query(cls)
                if self.sort_sql:
                    q = q.order_by(self.sort_sql)
                items = q.all()
                all = list()
                for item in items:
                    all.append([(getattr(item, col)) for col in self.cols.split(",")])
                for opt in all:
                    html.append("<option value='%s'>%s</option>" % (opt[0], opt[1]))
        else:
            obj = import_object(self.query_class)()
            if hasattr(obj, "data"):
                items = getattr(obj, "data")()
                for item in items:
                    html.append("<option value='%s'>%s</option>" % (item[0], item[1]))
        html.append("</select>")
        return "".join(html)


@ui("DataTable")
class DataTableModule(IWidget):
    __filter_mapping__ = dict()
    __entity_mapping__ = dict()
    __default_search_fields__ = dict()
    __security_points__ = dict()

    def render(self, **prop):
        self.dom_id = prop.get("id")#client dom id
        self.cols = prop.get("cols")#entity field list
        self.titles = prop.get("titles")#title list
        self.entity_full_name = prop.get("entity")#entity name
        self.form_id = prop.get("form")#Edit form id
        self.search_fields = prop.get("search_fields")#default search field name,and text type,
        self.point = EmptyClass()
        self.point.list = prop.get("point_list")
        self.point.add = prop.get("point_add")
        self.point.update = prop.get("point_update")
        self.point.delete = prop.get("point_delete")

        if not self.form_id:
            self.form_id = ""
        if not self.entity_full_name:
            return "Require entity full name."
        self.datatable_key = Utils.md5(self.entity_full_name)
        DataTableModule.__security_points__[self.datatable_key] = self.point
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
        opt["point"] = self.point
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
                {"mData": col, "sTitle": self.titles[index], "sClass": "datatable_column_" + col,
                 "sDefaultContent": ""})
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
        #items.append("/static/jslib/datatable/extras/tabletools/js/ZeroClipboard.js")
        #items.append("/static/jslib/datatable/extras/tabletools/js/TableTools.min.js")
        items.append("/static/jslib/tinyms.datatable.js")
        return items

    def css_files(self):
        items = list();
        #items.append("/static/jslib/datatable/css/jquery.dataTables.css")
        #items.append("/static/jslib/datatable/extras/tabletools/css/TableTools.css")
        return items


@route(r"/datatable/(.*)/(.*)")
class DataTableHandler(IRequest):
    def post(self, id, act):
        point = DataTableModule.__security_points__.get(id)
        message = dict()
        if act == "list":
            if not self.auth({point.list}):
                self.write(dict())
            else:
                self.list(id)
        elif act == "save":
            if not self.auth({point.update}):
                message["success"] = False
                message["msg"] = "UnAuth"
                self.write(json.dumps(message))
            else:
                self.update(id)
        elif act == "saveNext":
            if not self.auth({point.update}):
                message["success"] = False
                message["msg"] = "UnAuth"
                self.write(json.dumps(message))
            else:
                self.update(id)
        elif act == "delete":
            if not self.auth({point.delete}):
                message["success"] = False
                message["msg"] = "UnAuth"
                self.write(json.dumps(message))
            else:
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
        message = dict()
        self.set_header("Content-Type", "text/json;charset=utf-8")
        meta = DataTableModule.__entity_mapping__.get(id)
        if not meta:
            self.set_status(403, "Error!")
        entity = import_object(meta["name"])
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
        sort_params = self.parse_sort_params()
        order_sqlwhere = ""
        for k, v in sort_params.items():
            order_sqlwhere += "1=1 ORDER BY %s %s" % (k, v)
            break

        #DataGrid数据查询段落
        cnn = SessionFactory.new()
        #here place custom filter
        total_query = cnn.query(func.count(entity.id))
        ds_query = cnn.query(entity)
        custom_filter = DataTableModule.__filter_mapping__.get(meta["name"])
        if custom_filter:
            custom_filter_obj = custom_filter()
            if hasattr(custom_filter_obj, "total_filter"):
                total_query = custom_filter_obj.total_filter(total_query, self)
            if hasattr(custom_filter_obj, "dataset_filter"):
                ds_query = custom_filter_obj.dataset_filter(ds_query, self)
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


    def parse_sort_params(self):
        params = dict()
        colIndex = Utils.parse_int(self.get_argument("iSortCol_0"))
        direct = self.get_argument("sSortDir_0")
        params[self.datatable_display_cols[colIndex]] = direct
        return params

@ui("OrgTree")
class OrgTree(IWidget):
    def render(self, account_id = None):
        opt = dict()
        return self.render_string("widgets/orgtree.tpl",opt = opt)

    def css_files(self):
        items = list()
        items.append("/static/jslib/ztree/zTreeStyle.css")
        return items
    def javascript_files(self):
        items = list()
        items.append("/static/jslib/ztree/jquery.ztree.core-3.5.min.js")
        items.append("/static/jslib/ztree/jquery.ztree.exedit-3.5.min.js")
        items.append("/static/jslib/ztree/jquery.ztree.excheck-3.5.min.js")
        return items
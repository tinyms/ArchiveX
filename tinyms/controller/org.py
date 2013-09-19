__author__ = 'tinyms'

from tinyms.core.point import ajax,ObjectPool
from tinyms.dao.category import CategoryHelper
from tinyms.dao.account import AccountHelper

@ajax("OrgEdit")
class OrgEdit():
    __export__ = ["list","add","update","delete"]

    def list(self):
        tt = self.param("taxonomy")
        if not AccountHelper.auth(self.request.current_user,{ObjectPool.treeview[tt].list}):
            return []
        category = CategoryHelper(tt)
        simple_nodes = category.list()
        return simple_nodes

    def add(self):
        tt = self.param("taxonomy")
        if not AccountHelper.auth(self.request.current_user,{ObjectPool.treeview[tt].add}):
            return ["UnAuth"]
        parent_id = self.param("parent_id")
        cat_name = self.param("cat_name")
        category = CategoryHelper(tt)
        if category.exists(cat_name):
            return ["Exists"]
        id = category.create(cat_name,parent_id)
        return [id]

    def update(self):
        tt = self.param("taxonomy")
        if not AccountHelper.auth(self.request.current_user,{ObjectPool.treeview[tt].update}):
            return ["UnAuth"]
        id = self.param("id")
        parent_id = self.param("pId")
        cat_name = self.param("name")
        category = CategoryHelper(tt)
        if category.exists_other(id,cat_name):
            return ["Exists"]
        msg = category.update(id,cat_name,parent_id)
        return [msg]

    def delete(self):
        tt = self.param("taxonomy")
        if not AccountHelper.auth(self.request.current_user,{ObjectPool.treeview[tt].delete}):
            return ["UnAuth"]
        id = self.param("id")
        category = CategoryHelper(tt)
        return [category.remove(id)]
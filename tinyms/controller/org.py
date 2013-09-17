__author__ = 'tinyms'

import json
from tinyms.core.common import Utils
from tinyms.core.point import ajax,auth
from tinyms.dao.category import CategoryHelper

@ajax("OrgEdit")
class OrgEdit():
    __export__ = ["list","add","update","delete"]

    def list(self):
        category = CategoryHelper()
        simple_nodes = category.list()
        print(simple_nodes)
        return simple_nodes

    def add(self):
        parent_id = self.param("parent_id")
        cat_name = self.param("cat_name")
        category = CategoryHelper()
        if category.exists(cat_name):
            return ["Exists"]
        id = category.create(cat_name,parent_id)
        return [id]

    def update(self):
        id = self.param("id")
        parent_id = self.param("parent_id")
        cat_name = self.param("cat_name")
        category = CategoryHelper()
        if category.exists_other(cat_name):
            return ["Exists"]
        msg = category.update(id,cat_name,parent_id)
        return [msg]

    def delete(self):
        id = self.param("id")
        category = CategoryHelper()
        return [category.remove(id)]
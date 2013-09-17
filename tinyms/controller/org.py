__author__ = 'tinyms'

import json
from tinyms.core.common import Utils
from tinyms.core.point import ajax,auth
from tinyms.dao.category import CategoryHelper

@ajax("OrgEdit")
class OrgEdit():
    __export__ = ["list","save","delete"]

    def list(self):
        pass

    def save(self):
        parent_id = self.param("parent_id")
        cat_name = self.param("cat_name")
        helper = CategoryHelper()
        if helper.exists(cat_name,parent_id):
            return ["Exists"]
        new_cat_id = helper.create_or_update_category(cat_name,parent_id)
        if not new_cat_id:
            return ["-1"]
        return ["%s" % new_cat_id]

    def delete(self):
        pass
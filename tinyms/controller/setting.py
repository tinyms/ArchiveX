__author__ = 'tinyms'

from tinyms.core.web import IAuthRequest
from tinyms.core.point import ObjectPool, route, setting


@route("/workbench/setting")
class SettingPage(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/setting.html")

    def post(self, *args, **kwargs):
        kv = self.wrap_params_to_dict()
        items = ObjectPool.setting
        for item in items:
            obj = item.cls()
            if hasattr(obj, "save"):
                obj.save(kv, self)
        pass


@setting("tinyms.core.sys.setting", "workbench/sys_setting_page", "全局")
class SystemSetting():
    def save(self, kv, http_req):
        pass
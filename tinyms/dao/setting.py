__author__ = 'tinyms'

import json

from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Setting
from tinyms.core.common import JsonEncoder


class UserSettingHelper():
    def __init__(self, usr_id):
        self.usr = usr_id
        cnn = SessionFactory.new()
        json_text = cnn.query(Setting.val_).filter(Setting.owner_ == self.usr).limit(1).scalar()
        if json:
            self.setting = json.loads(json_text, encoding="utf8", cls=JsonEncoder)
        else:
            self.setting = dict()

    def get(self, key, default_=None):
        val = self.setting.get(key)
        if val:
            return val
        return default_

    def set(self, key, val):
        cnn = SessionFactory.new()
        item = cnn.query(Setting).filter(Setting.key_ == key).limit(1).scalar()
        if item:
            item.val_ = val
            cnn.commit()
        else:
            obj = Setting()
            obj.key_ = key
            obj.val_ = val
            cnn.add(obj)
            cnn.commit()


class AppSettingHelper():
    __global__ = dict()

    @staticmethod
    def get(default_=None):
        return UserSettingHelper.get("root", default_)

    @staticmethod
    def set(val):
        return UserSettingHelper.set("root", val)

    pass

__author__ = 'tinyms'

from datetime import datetime
from sqlalchemy import func
from tinyms.core.common import Utils
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Role, Archives, Account, SecurityPoint
from tinyms.core.point import ObjectPool,reg


class Loader():
    @staticmethod
    def init():
        role_ = Loader.create_super_role()
        if not role_:
            return
        Loader.create_root_account(role_)
        Loader.create_base_securitypoints()
        Loader.assign_points_to__superadmin(role_)
    @staticmethod
    def create_root_account(super_role):
        cnn = SessionFactory.new()
        num = cnn.query(func.count(Archives.id)).scalar()
        if num == 0:
            usr = Archives()
            usr.name = "超级管理员"
            usr.email = "admin@local.com"
            cnn.add(usr)
            cnn.commit()

            a = Account()
            a.login_name = "root"
            a.login_pwd = Utils.md5("root")
            a.create_time = datetime.now()
            a.enabled = True
            a.archives_id = usr.id
            cnn.add(a)
            role_ = cnn.query(Role).get(super_role.id)
            a.roles.append(role_)
            cnn.commit()

    @staticmethod
    def create_super_role():
        cnn = SessionFactory.new()
        role_ = cnn.query(Role).filter(Role.name == "SuperAdmin").limit(1).scalar()
        if role_:
            return role_
        role_ = Role()
        role_.name = "SuperAdmin"
        role_.description = "超级管理员"
        cnn.add(role_)
        cnn.commit()
        return role_

    @staticmethod
    def assign_points_to__superadmin(super_role):
        cnn = SessionFactory.new()
        role_ = cnn.query(Role).get(super_role.id)
        changes = list()
        for point in ObjectPool.points:
            p = cnn.query(SecurityPoint).filter(SecurityPoint.key_ == point.key_).limit(1).scalar()
            if p:
                p.category = point.category
                p.group_ = point.group_
                p.description = point.description
                changes.append(p)
            else:
                cnn.add(point)
                point.roles.append(role_)
        cnn.commit()

    @staticmethod
    def create_base_securitypoints():
        reg("archives_list","人员管理","档案","查看档案列表")
        reg("archives_add","人员管理","档案","添加人员档案")
        reg("archives_update","人员管理","档案","修改人员档案")
        reg("archives_delete","人员管理","档案","删除人员档案")
        pass
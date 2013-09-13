__author__ = 'tinyms'

from datetime import datetime
from sqlalchemy import func
from tinyms.core.common import Utils
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Role, Archives, Account, SecurityPoint
from tinyms.core.point import ObjectPool,reg_point


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
        role_ = cnn.query(Role).get(super_role.id)
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
        reg_point("tinyms.sidebar.archives.show","菜单","侧边栏","人员档案")
        reg_point("tinyms.sidebar.role_org.show","菜单","侧边栏","角色组织")
        reg_point("tinyms.sidebar.sys_params.show","菜单","侧边栏","系统参数")
        reg_point("tinyms.entity.role.list","角色组织","角色","查看角色列表")
        reg_point("tinyms.entity.role.add","角色组织","角色","添加角色")
        reg_point("tinyms.entity.role.update","角色组织","角色","修改角色")
        reg_point("tinyms.entity.role.delete","角色组织","角色","删除角色")
        reg_point("tinyms.entity.role.points.view","角色组织","权限","查看角色权限点")
        reg_point("tinyms.entity.role.points.update","角色组织","权限","修改角色权限")
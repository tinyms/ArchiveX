__author__ = 'tinyms'
#coding=UTF8
from datetime import datetime
from sqlalchemy import func
from tinyms.core.common import Utils
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Role, Archives, Account, SecurityPoint
from tinyms.core.annotation import ObjectPool, reg_point
from tinyms.dao.category import CategoryHelper
from tinyms.core.setting import AppSettingHelper


#Web服务器加载时，初始化必要数据
class Loader():
    @staticmethod
    def init():
        AppSettingHelper.load()
        #Create Root Category
        helper = CategoryHelper("ROOT")
        if not helper.exists("ROOT"):
            helper.create("ROOT")
        role_id = Loader.create_super_role()
        if not role_id:
            return
        Loader.create_root_account(role_id)
        Loader.create_base_securitypoints()
        Loader.assign_points_to_superadmin(role_id)
        #自定义加载
        for cls in ObjectPool.server_starups:
            obj = cls()
            if hasattr(obj, "load"):
                obj.load()

    @staticmethod
    def create_root_account(role_id):
        cnn = SessionFactory.new()
        num = cnn.query(func.count(Archives.id)).scalar()
        role_ = cnn.query(Role).get(role_id)
        if num == 0:
            usr = Archives()
            usr.name = u"超级管理员"
            usr.email = "admin@local.com"
            usr.code = "P00001"
            cnn.add(usr)
            cnn.commit()

            a = Account()
            a.login_name = "root"
            a.login_pwd = Utils.md5("root")
            a.create_time = datetime.now()
            a.enabled = 1
            a.archives_id = usr.id
            cnn.add(a)
            a.roles.append(role_)
            cnn.commit()

    @staticmethod
    def create_super_role():
        cnn = SessionFactory.new()
        role_ = cnn.query(Role).filter(Role.name == "SuperAdmin").limit(1).scalar()
        if role_:
            return role_.id
        role_ = Role()
        role_.name = "SuperAdmin"
        role_.description = u"超级管理员"
        cnn.add(role_)
        cnn.commit()
        return role_.id

    @staticmethod
    def assign_points_to_superadmin(role_id):
        cnn = SessionFactory.new()
        role_ = cnn.query(Role).get(role_id)
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
        #Menu
        reg_point("tinyms.sidebar.archives.show", u"菜单", u"侧边栏", u"人员档案")
        reg_point("tinyms.sidebar.role_org.show", u"菜单", u"侧边栏", u"角色组织")
        reg_point("tinyms.sidebar.sys_categories.show", u"菜单", u"侧边栏", u"系统分类")
        reg_point("tinyms.sidebar.sys_params.show", u"菜单", u"侧边栏", u"系统参数")
        #OrgTreeView
        reg_point("tinyms.view.orgtree.list", u"角色组织", u"组织", u"查看组织列表")
        reg_point("tinyms.view.orgtree.view", u"角色组织", u"组织", u"查看组织明细")
        reg_point("tinyms.view.orgtree.add", u"角色组织", u"组织", u"添加组织")
        reg_point("tinyms.view.orgtree.update", u"角色组织", u"组织", u"修改组织")
        reg_point("tinyms.view.orgtree.delete", u"角色组织", u"组织", u"删除组织")
        #分类管理
        reg_point("tinyms.view.termtaxonomy.list", u"角色组织", u"分类", u"查看分类列表")
        reg_point("tinyms.view.termtaxonomy.view", u"角色组织", u"分类", u"查看分类明细")
        reg_point("tinyms.view.termtaxonomy.add", u"角色组织", u"分类", u"添加分类")
        reg_point("tinyms.view.termtaxonomy.update", u"角色组织", u"分类", u"修改分类")
        reg_point("tinyms.view.termtaxonomy.delete", u"角色组织", u"分类", u"删除分类")
        #角色管理
        reg_point("tinyms.entity.role.list", u"角色组织", u"角色", u"查看角色列表")
        reg_point("tinyms.entity.role.view", u"角色组织", u"角色", u"查看角色明细")
        reg_point("tinyms.entity.role.add", u"角色组织", u"角色", u"添加角色")
        reg_point("tinyms.entity.role.update", u"角色组织", u"角色", u"修改角色")
        reg_point("tinyms.entity.role.delete", u"角色组织", u"角色", u"删除角色")
        reg_point("tinyms.entity.role.points.view", u"角色组织", u"权限", u"查看角色权限点")
        reg_point("tinyms.entity.role.points.update", u"角色组织", u"权限", u"修改角色权限")
        #账户管理
        reg_point("tinyms.entity.account.list", u"角色组织", u"账户", u"查看账户列表")
        reg_point("tinyms.entity.account.view", u"角色组织", u"账户", u"查看账户明细")
        reg_point("tinyms.entity.account.add", u"角色组织", u"账户", u"添加账户")
        reg_point("tinyms.entity.account.update", u"角色组织", u"账户", u"修改账户")
        reg_point("tinyms.entity.account.delete", u"角色组织", u"账户", u"删除账户")
        reg_point("tinyms.entity.account.role.view", u"角色组织", u"账户", u"查看账户角色")
        reg_point("tinyms.entity.account.role.edit", u"角色组织", u"账户", u"为账户设置角色")
        #档案管理
        reg_point("tinyms.entity.archives.list", u"档案管理", u"人员", u"查看人员列表")
        reg_point("tinyms.entity.archives.view", u"档案管理", u"人员", u"查看人员明细")
        reg_point("tinyms.entity.archives.add", u"档案管理", u"人员", u"添加人员")
        reg_point("tinyms.entity.archives.update", u"档案管理", u"人员", u"修改人员")
        reg_point("tinyms.entity.archives.delete", u"档案管理", u"人员", u"删除人员")
        #档案管理
        reg_point("tinyms.entity.setting.system", u"系统设置", u"设置", u"全局设置")
        reg_point("tinyms.entity.setting.user", u"系统设置", u"设置", u"用户自定义设置")

        for cls in ObjectPool.user_security_points:
            obj = cls()
            if hasattr(obj, "reg"):
                obj.reg()



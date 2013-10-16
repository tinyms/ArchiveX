__author__ = 'tinyms'

import json
from sqlalchemy import or_
from tinyms.core.common import Utils
from tinyms.core.web import IAuthRequest
from tinyms.core.point import route,ajax,auth,dataview_provider
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import SecurityPoint,Role,Account,Archives

@ajax("RoleSecurityPointsAssign")
class RoleSecurityPointsEdit():
    __export__ = ["list","save"]

    @auth({"tinyms.entity.role.points.view"},[])
    def list(self):
        role_id = self.param("id")
        if not role_id:
            return []
        cnn = SessionFactory.new()
        points = cnn.query(SecurityPoint.id).join((Role,SecurityPoint.roles)).filter(Role.id == role_id).all()
        return [p[0] for p in points]

    @auth({"tinyms.entity.role.points.update"},["UnAuth"])
    def save(self):
        role_id = self.param("id")
        if not role_id:
            return ["Error"]
        points = json.loads(self.param("points"))
        cnn = SessionFactory.new()
        role = cnn.query(Role).filter(Role.id==role_id).limit(1).scalar()
        if role and not role.name=="SuperAdmin":
            role.securitypoints = []
            cnn.commit()
            spoints = cnn.query(SecurityPoint).filter(SecurityPoint.id.in_(points)).all()
            for sp in spoints:
                role.securitypoints.append(sp)
            cnn.commit()
        return ["Success"]
    pass

@route("/workbench/security")
class RoleOrg(IAuthRequest):
    def get(self, *args, **kwargs):
        context = dict()
        categories = self.role_categories()
        all = list()
        for c in categories:
            sub = list()
            groups = self.role_groups(c)
            for g in groups:
                sub.append((g, self.points(c, g)))
                pass
            all.append((c, sub, Utils.md5(c)))

        context["categories"] = all
        context["roles_for_account"] = self.role_for_account()
        return self.render("workbench/role_org.html", data=context)

    #列出可用角色
    def role_for_account(self):
        cnn = SessionFactory.new()
        items = cnn.query(Role.id,Role.name).all()
        print(items)
        return items

    def role_categories(self):
        cnn = SessionFactory.new()
        items = cnn.query(SecurityPoint.category).group_by(SecurityPoint.category).order_by(
            SecurityPoint.id.asc()).all()
        categories = [(cat[0]) for cat in items]
        return categories

    def role_groups(self, c):
        cnn = SessionFactory.new()
        items = cnn.query(SecurityPoint.group_).filter(SecurityPoint.category == c).\
            group_by(SecurityPoint.group_).order_by(SecurityPoint.id.asc()).all()
        groups = [item[0] for item in items]
        return groups

    def points(self, c, g):
        cnn = SessionFactory.new()
        items = cnn.query(SecurityPoint).filter(SecurityPoint.category == c).filter(SecurityPoint.group_ == g).order_by(
            SecurityPoint.id.asc()).all()
        return items

#账户管理数据提供
@dataview_provider("tinyms.core.view.AccountManager")
class AccountDataProvider():

    def count(self,session,default_search_val,http_req):
        q = session.query(Account,Archives.name,Archives.email).outerjoin(Archives,Account.archives_id==Archives.id)
        if default_search_val:
            q = q.filter(or_(Account.login_name.like('%'+default_search_val+'%'),Archives.name.like('%'+default_search_val+'%'),Archives.email.like('%'+default_search_val+'%')))
        return q.count()

    def list(self,session,default_search_val,http_req,start,limit):
        q = session.query(Account,Archives.name,Archives.email).outerjoin(Archives,Account.archives_id==Archives.id)
        if default_search_val:
            q = q.filter(or_(Account.login_name.like('%'+default_search_val+'%'),Archives.name.like('%'+default_search_val+'%'),Archives.email.like('%'+default_search_val+'%')))
        ds = q.offset(start).limit(limit).all()
        items = list()
        for row in ds:
            item = dict()
            obj = row[0].dict()
            item["id"] = obj["id"]
            item["archives_id"] = obj["archives_id"]
            item["login_name"] = obj["login_name"]
            item["enabled"] = obj["enabled"]
            item["last_logon_time"] = Utils.format_datetime_short(obj["last_logon_time"])
            item["create_time"] = Utils.format_datetime_short(obj["create_time"])
            item["name"] = row[1]
            item["email"] = row[2]
            items.append(item)
        print(items)
        return items
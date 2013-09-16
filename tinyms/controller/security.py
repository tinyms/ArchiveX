__author__ = 'tinyms'

import json
from tinyms.core.common import Utils
from tinyms.core.web import IAuthRequest
from tinyms.core.point import route,ajax,auth
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import SecurityPoint,Role

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
        return self.render("workbench/role_org.html", data=context)

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
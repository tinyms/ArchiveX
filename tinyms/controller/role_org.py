__author__ = 'tinyms'

from tinyms.core.common import Utils
from tinyms.core.web import IAuthRequest
from tinyms.core.point import route
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import SecurityPoint


@route("/workbench/security")
class RoleOrg(IAuthRequest):
    def get(self, *args, **kwargs):
        categories = self.role_categories()

        all = list()
        for c in categories:
            sub = list()
            groups = self.role_groups(c)
            for g in groups:
                sub.append((g, self.points(c, g)))
                pass
            all.append((c, sub, Utils.md5(c)))
        context = dict()
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
__author__ = 'tinyms'

from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Account, Role, SecurityPoint, Archives


class AccountHelper():
    @staticmethod
    def points(account_id=None):
        tmp = set()
        if not account_id:
            return tmp
        cnn = SessionFactory.new()
        all = cnn.query(SecurityPoint.key_) \
            .join((Role, Account.roles)).join((SecurityPoint, Role.securitypoints)).filter(
            Account.id == account_id).all()

        for p in all:
            tmp.add(p[0])
        return tmp

    @staticmethod
    def auth(account_id=None,points={}):
        if len(points & AccountHelper.points(account_id)) > 0:
            return True
        return False

    @staticmethod
    def name(account_id=None):
        if not account_id:
            return ""
        cnn = SessionFactory.new()
        return cnn.query(Archives.name).join(Account)\
            .filter(Archives.id==Account.archives_id).filter(Account.id==account_id).limit(1).scalar()

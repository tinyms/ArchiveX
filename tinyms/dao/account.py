__author__ = 'tinyms'

from tinyms.core.orm import SessionFactory
from tinyms.core.common import Utils
from tinyms.core.entity import Account, Role, SecurityPoint, Archives


class AccountHelper():
    @staticmethod
    def create(login_id, pwd, archives_id=None, enabled=0):
        cnn = SessionFactory.new()
        obj = Account()
        obj.login_name = login_id
        obj.login_pwd = Utils.md5(pwd)
        obj.create_time = Utils.current_datetime()
        obj.enabled = enabled
        obj.archives_id = archives_id
        cnn.add(obj)
        cnn.commit()
        return obj.id

    @staticmethod
    def update(id, login_id, pwd, archives_id=None, enabled=False):
        cnn = SessionFactory.new()
        a = cnn.query(Account).get(id)
        a.login_name = login_id
        if pwd:
            a.login_pwd = Utils.md5(pwd)
        a.enabled = enabled
        a.archives_id = archives_id
        cnn.commit()
        return "Updated"

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
    def auth(account_id=None, points={}):
        if len(points & AccountHelper.points(account_id)) > 0:
            return True
        return False

    @staticmethod
    def name(account_id=None):
        if not account_id:
            return ""
        cnn = SessionFactory.new()
        return cnn.query(Archives.name).join(Account) \
            .filter(Archives.id == Account.archives_id).filter(Account.id == account_id).limit(1).scalar()

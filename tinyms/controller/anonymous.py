__author__ = 'tinyms'

from tinyms.core.point import route
from tinyms.core.web import IRequest
from tinyms.core.common import Utils
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Account,Archives,Role,SecurityPoint

@route("/login")
class Login(IRequest):

    def get(self, *args, **kwargs):
        """
        render login form
        :param args:
        :param kwargs:
        """
        self.render("login.html")
    def post(self, *args, **kwargs):
        """
        do login action
        :param args:
        :param kwargs:
        """
        login_id = self.get_argument("login_id")
        login_pwd = self.get_argument("login_pwd")
        if not login_id or not login_pwd:
            self.redirect(self.get_login_url())
        cnn = SessionFactory.new()

        if Utils.is_email(Utils.trim(login_id)):
            current_account = cnn.query(Account).join(Archives).filter(Account.archivex_id==Archives.id)\
                .filter(Account.login_name==login_id).filter(Account.login_pwd==Utils.md5(login_pwd)).limit(1).scalar()
        else:
            current_account = cnn.query(Account)\
                .filter(Account.login_name==login_id).filter(Account.login_pwd==Utils.md5(login_pwd)).limit(1).scalar()

        if current_account:
            print(current_account)
            name = cnn.query(Archives.name).filter(Archives.id==current_account.archives_id).limit(1).scalar()
            points = cnn.query(SecurityPoint.key_)\
                .join((Role,Account.roles)).join((SecurityPoint,Role.securitypoints)).filter(Account.id==current_account.id).all()
            print(name,points)

        self.render("login.html")

@route("/logout")
class Logout(IRequest):
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect("/login")
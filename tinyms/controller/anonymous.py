__author__ = 'tinyms'

from tinyms.core.point import route
from tinyms.core.web import IRequest
from tinyms.core.common import Utils
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Account,Archives

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
            rows = cnn.query(Account.id,Archives.name).outerjoin(Archives,Account.archives_id==Archives.id)\
                .filter(Archives.email==login_id).filter(Account.login_pwd==Utils.md5(login_pwd)).filter(Account.enabled==1).limit(1).all()
            if len(rows)>0:
                id = rows[0][0]
                name = rows[0][1]
                self.set_secure_cookie(IRequest.__key_account_id__,"%i" % id)
                self.set_secure_cookie(IRequest.__key_account_name__,name)
                self.update_last_login_datetime(id)
        else:
            rows = cnn.query(Account.id,Archives.name).outerjoin(Archives,Account.archives_id==Archives.id)\
                .filter(Account.login_name==login_id).filter(Account.login_pwd==Utils.md5(login_pwd)).filter(Account.enabled==1).limit(1).all()
            if len(rows)>0:
                id = rows[0][0]
                name = rows[0][1]
                self.set_secure_cookie(IRequest.__key_account_id__,"%i" % id)
                self.set_secure_cookie(IRequest.__key_account_name__,name)
                self.update_last_login_datetime(id)

        self.redirect("/workbench/dashboard")

    def update_last_login_datetime(self,id):
        cnn = SessionFactory.new()
        a = cnn.query(Account).get(id)
        a.last_logon_time = Utils.current_datetime()
        cnn.commit()

@route("/logout")
class Logout(IRequest):
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect("/login")
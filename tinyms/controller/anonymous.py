__author__ = 'tinyms'

from tinyms.core.point import route
from tinyms.core.web import IRequest

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
        pass

@route("/logout")
class Logout(IRequest):
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect("/login")
__author__ = 'tinyms'

from tinyms.core.common import Utils
from tinyms.core.web import IAuthRequest
from tinyms.core.point import route, ajax, auth
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Archives, Account

@route("/workbench/archives")
class ArchiveController(IAuthRequest):

    def get(self, *args, **kwargs):
        return self.render("workbench/archives.html")

@route("/workbench/categories")
class TermTaxonomyController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/categories.html")
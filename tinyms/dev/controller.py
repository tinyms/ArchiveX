__author__ = 'tinyms'

from tinyms.core.annotation import route
from tinyms.core.web import IAuthRequest


@route("/workbench/dev/project")
class ProjectController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/dev.project.html")


@route("/workbench/dev/widgets")
class WidgetsController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/dev.widgets.html")


@route("/workbench/dev/entity")
class EntityController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/dev.entity.html")
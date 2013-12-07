__author__ = 'tinyms'

from sqlalchemy.engine import reflection
from tinyms.core.orm import SessionFactory
from tinyms.core.annotation import route
from tinyms.core.web import IAuthRequest
from tinyms.core.common import Utils


@route("/workbench/dev/project")
class ProjectController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/dev.project.html")


@route("/workbench/dev/widgets")
class WidgetsController(IAuthRequest):
    def get(self, *args, **kwargs):
        insp = reflection.Inspector.from_engine(SessionFactory.__engine__)
        context_data = dict()
        context_data["entity_map"] = Utils.encode(SessionFactory.entitys)
        table_cols = dict()
        for entity in SessionFactory.entitys:
            table_name = SessionFactory.entitys[entity]
            cols_def = insp.get_columns(table_name)
            cols = list()
            for col_def in cols_def:
                cols.append(col_def["name"])
            table_cols[table_name] = cols
        context_data["table_cols"] = table_cols
        return self.render("workbench/dev.widgets.html", context=context_data)


@route("/workbench/dev/entity")
class EntityController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/dev.entity.html")
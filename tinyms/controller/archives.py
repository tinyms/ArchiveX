__author__ = 'tinyms'

from sqlalchemy import func

from tinyms.core.common import Utils
from tinyms.core.web import IAuthRequest
from tinyms.core.point import route, datatable_provider
from tinyms.core.entity import WorkExperience, LearningExperience, TrainingExperience, Archives
from tinyms.core.setting import AppSettingHelper


@route("/workbench/archives")
class ArchiveController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/archives.html")


@route("/workbench/categories")
class TermTaxonomyController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/categories.html")


@datatable_provider("tinyms.core.entity.Archives")
class ArchivesDataProvider():

    def total(self, query, req):
        return query.filter(Archives.name != "超级管理员")

    def dataset(self, query, req):
        return query.filter(Archives.name != "超级管理员")

    def after_add(self, entity_obj, sf, req):
        length = len(str(sf.query(func.count(Archives.id)).scalar()))
        obj = sf.query(Archives).get(entity_obj.id)
        max_length = AppSettingHelper.get("s_usr_code_fmt_length", "5")
        prefix = AppSettingHelper.get("s_usr_code_prefix", "P")
        if length > Utils.parse_int(max_length):
            max_length = "%s" % (length + 1)
        fmt = prefix + "%0" + max_length + "d"
        obj.code = fmt % entity_obj.id
        sf.commit()

    def before_add(self, entity_obj, sf, req):
        if entity_obj.email:
            num = sf.query(func.count(Archives.id)).filter(Archives.email == entity_obj.email).scalar()
            if num > 0:
                return "EmailExists"
        return ""

    def before_modify(self, entity_obj, sf, req):
        if entity_obj.email:
            num = sf.query(func.count(Archives.id)).filter(Archives.email == entity_obj.email).scalar()
            if num > 0:
                return "EmailExists"
        return ""


@datatable_provider("tinyms.core.entity.WorkExperience")
class WorkExperienceDataTableFilter():
    def total(self, query, req):
        return query.filter(WorkExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))

    def dataset(self, query, req):
        return query.filter(WorkExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))


@datatable_provider("tinyms.core.entity.LearningExperience")
class LearningExperienceDataTableFilter():
    def total(self, query, req):
        return query.filter(LearningExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))

    def dataset(self, query, req):
        return query.filter(LearningExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))


@datatable_provider("tinyms.core.entity.TrainingExperience")
class TrainingExperienceDataTableFilter():
    def total(self, session, req):
        return session.filter(TrainingExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))

    def dataset(self, session, req):
        return session.filter(TrainingExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))
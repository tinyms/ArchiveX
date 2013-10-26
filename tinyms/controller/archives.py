__author__ = 'tinyms'

from tinyms.core.common import Utils
from tinyms.core.web import IAuthRequest
from tinyms.core.point import route, datatable_provider
from tinyms.core.entity import WorkExperience, LearningExperience, TrainingExperience


@route("/workbench/archives")
class ArchiveController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/archives.html")


@route("/workbench/categories")
class TermTaxonomyController(IAuthRequest):
    def get(self, *args, **kwargs):
        return self.render("workbench/categories.html")


@datatable_provider("tinyms.core.entity.WorkExperience")
class WorkExperienceDataTableFilter():
    def total(self, session, req):
        return session.filter(WorkExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))

    def dataset(self, session, req):
        return session.filter(WorkExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))


@datatable_provider("tinyms.core.entity.LearningExperience")
class LearningExperienceDataTableFilter():
    def total(self, session, req):
        return session.filter(LearningExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))

    def dataset(self, session, req):
        return session.filter(LearningExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))


@datatable_provider("tinyms.core.entity.TrainingExperience")
class TrainingExperienceDataTableFilter():
    def total(self, session, req):
        return session.filter(TrainingExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))

    def dataset(self, session, req):
        return session.filter(TrainingExperience.archives_id == Utils.parse_int(req.get_argument("archives_id")))
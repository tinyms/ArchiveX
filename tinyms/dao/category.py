__author__ = 'tinyms'

from sqlalchemy import func
from tinyms.core.common import Utils
from tinyms.core.orm import SessionFactory
from tinyms.core.entity import Term, TermTaxonomy


class CategoryHelper():
    def __init__(self, taxonomy="Org"):
        self.taxonomy = taxonomy

    def create_term(self, name):
        name_ = Utils.trim(name)
        cnn = SessionFactory.new()
        id = cnn.query(Term.id).filter(Term.name == name_).limit(1).scalar()
        if not id:
            term = Term()
            term.name = name_
            term.slug = name_
            cnn.add(term)
            cnn.commit()
            return term.id
        return id

    def create_or_update_category(self, name_, parent_id=None):
        term_id = self.create_term(name_)
        parent_path = self.get_path(parent_id)
        cnn = SessionFactory.new()
        exists_tt = cnn.query(TermTaxonomy).filter(TermTaxonomy.term_id == term_id) \
            .filter(TermTaxonomy.taxonomy == self.taxonomy).limit(1).scalar()
        if not exists_tt:
            tt = TermTaxonomy()
            tt.parent_id = parent_id
            tt.term_id = term_id
            tt.taxonomy = self.taxonomy
            tt.object_count = 0
            tt.path = parent_path
            cnn.add(tt)
            cnn.commit()
            tt.path = "%s/%s" % (parent_path, tt.id)
            cnn.commit()
            return tt.id
        else:
            exists_tt.term_id = term_id
            exists_tt.parent_id = parent_id
            cnn.commit()
            return exists_tt.id

    def exists(self, name_, parent_id=None):
        cnn = SessionFactory.new()
        num = cnn.query(func.count(TermTaxonomy.id)).filter(TermTaxonomy.term.name == Utils.trim(name_)) \
            .filter(TermTaxonomy.taxonomy == self.taxonomy).filter(TermTaxonomy.parent_id == parent_id)\
            .limit(1).scalar()
        if num > 0:
            return True
        return False


    def get_path(self, id):
        cnn = SessionFactory.new()
        path = cnn.query(TermTaxonomy.path).filter(TermTaxonomy.id == id).limit(1).scalar()
        if not path:
            return "/"
        return path

    def get_name(self, id):
        cnn = SessionFactory.new()
        name = cnn.query(TermTaxonomy.term.name).filter(TermTaxonomy.id == id).limit(1).scalar()
        return name

    def get_object_count(self, id):
        cnn = SessionFactory.new()
        object_count = cnn.query(TermTaxonomy.object_count).filter(TermTaxonomy.id == id).limit(1).scalar()
        return object_count

    def set_object_count(self, id, chang_num=0):
        cnn = SessionFactory.new()
        tt = cnn.query(TermTaxonomy).filter(TermTaxonomy.id == id).limit(1).scalar()
        if tt:
            tt.object_count += chang_num
            cnn.commit()
            return True
        return False

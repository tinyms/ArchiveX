__author__ = 'tinyms'

import json
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref, class_mapper
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import sessionmaker

Entity = declarative_base()

class SessionFactory():
    __engine__ = None
    __table_name_prefix__ = ""
    @staticmethod
    def new():
        if SessionFactory.__engine__:
            return sessionmaker(bind=SessionFactory.__engine__)()
        return None

    @staticmethod
    def create_tables():
        if SessionFactory.__engine__:
            Entity.metadata.create_all(SessionFactory.__engine__)

class Simplify():
    """
    简化实体创建及可以JSON化实体数据
    """
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        return "%s_%s" % (SessionFactory.__table_name_prefix__,self.__name__.lower())

    def dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)

    def json(self):
        return json.dumps(self.dict())

    def __repr__(self):
        return "<%s%s>" % (self.__tablename__.capitalize(), self.dict())


def one_to_one(foreign_entity_name):
    """
    一对一，比如: 从表对主表
    一旦映射成功，彼此获取到对方表名实体对象变量，也就是你可以直接访问我，我可以直接访问你
    :param foreign_entity_name: 目标实体名
    :return:
    """
    def ref_table(cls):
        foreign_entity_name_lower = foreign_entity_name.lower()
        foreign_table_name = "%s_%s" % (SessionFactory.__table_name_prefix__,foreign_entity_name_lower)
        setattr(cls, '{0}_id'.format(foreign_entity_name_lower),
                Column(Integer, ForeignKey('{0}.id'.format(foreign_table_name), ondelete="CASCADE")))
        setattr(cls, foreign_entity_name_lower,
                relationship(foreign_entity_name,
                             backref=backref(cls.__name__.lower(), uselist=False, lazy='dynamic')))
        return cls

    return ref_table


def many_to_one(foreign_entity_name):
    """
    多对一，一对多共用这种形式
    一旦映射成功，one的一方将自动拥有many一方集合变量名`表名s`
    :param foreign_entity_name: 目标实体名
    :return:
    """
    def ref_table(cls):
        foreign_entity_name_lower = foreign_entity_name.lower()
        foreign_table_name = "%s_%s" % (SessionFactory.__table_name_prefix__,foreign_entity_name_lower)

        if foreign_entity_name == cls.__name__:
            foreign_entity_name_lower = "parent"
        setattr(cls, '{0}_id'.format(foreign_entity_name_lower),
                Column(Integer, ForeignKey('{0}.id'.format(foreign_table_name), ondelete="CASCADE")))
        setattr(cls, foreign_entity_name_lower,
                relationship(foreign_entity_name, backref=backref(cls.__name__.lower() + 's', lazy='dynamic')))
        return cls

    return ref_table


def many_to_many(foreign_entity_name):
    """
    多对多，装饰到有关联关系的任意实体之上
    一旦映射成功，彼此皆可获取对方`表名s`集合变量
    :param foreign_entity_name: 目标实体名
    :return:
    """
    def ref_table(cls):
        target_name = foreign_entity_name.lower()
        self_name = cls.__name__.lower()
        association_table = Table('{0}_association_{1}_{2}'.format(SessionFactory.__table_name_prefix__,self_name, target_name), Entity.metadata,
                                  Column('{0}_id'.format(target_name), Integer,
                                         ForeignKey('{0}_{1}.id'.format(SessionFactory.__table_name_prefix__,target_name),ondelete="CASCADE")),
                                  Column('{0}_id'.format(self_name), Integer,
                                         ForeignKey('{0}_{1}.id'.format(SessionFactory.__table_name_prefix__,self_name),ondelete="CASCADE"))
        )

        setattr(cls, target_name + 's',
                relationship(foreign_entity_name, secondary=association_table,
                             backref=backref(cls.__name__.lower() + 's', lazy='dynamic')))
        return cls

    return ref_table
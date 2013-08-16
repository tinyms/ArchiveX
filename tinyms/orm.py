__author__ = 'tinyms'
import json
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref, class_mapper
from sqlalchemy import create_engine, Column, Integer, ForeignKey, Table
from sqlalchemy.orm import sessionmaker

Entity = declarative_base()


class Simplify():
    """
    简化实体创建及可以JSON化实体数据
    """
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    def dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)

    def json(self):
        return json.dumps(self.dict())

    def __repr__(self):
        return "<%s%s>" % (self.__tablename__.capitalize(), self.dict())


def one_to_one(entity_name):
    """
    一对一，比如: 从表对主表
    一旦映射成功，彼此获取到对方表名实体对象变量，也就是你可以直接访问我，我可以直接访问你
    :param entity_name: 目标实体名
    :return:
    """
    def ref_table(cls):
        table_name = entity_name.lower()
        setattr(cls, '{0}_id'.format(table_name),
                Column(Integer, ForeignKey('{0}.id'.format(table_name), ondelete='CASCADE')))
        setattr(cls, table_name,
                relationship(table_name.capitalize(),
                             backref=backref(cls.__name__.lower(), uselist=False, lazy='dynamic')))
        return cls

    return ref_table


def many_to_one(entity_name):
    """
    多对一，一对多共用这种形式
    一旦映射成功，one的一方将自动拥有many一方集合变量名`表名s`
    :param entity_name: 目标实体名
    :return:
    """
    def ref_table(cls):
        table_name = entity_name.lower()
        setattr(cls, '{0}_id'.format(table_name),
                Column(Integer, ForeignKey('{0}.id'.format(table_name), ondelete='CASCADE')))
        setattr(cls, table_name,
                relationship(table_name.capitalize(), backref=backref(cls.__name__.lower() + 's', lazy='dynamic')))
        return cls

    return ref_table


def many_to_many(entity_name):
    """
    多对多，装饰到有关联关系的任意实体之上
    一旦映射成功，彼此皆可获取对方`表名s`集合变量
    :param entity_name: 目标实体名
    :return:
    """
    def ref_table(cls):
        target_name = entity_name.lower()
        self_name = cls.__name__.lower()
        association_table = Table('association_{0}_{1}'.format(self_name, target_name), Entity.metadata,
                                  Column('{0}_id'.format(target_name), Integer,
                                         ForeignKey('{0}.id'.format(target_name))),
                                  Column('{0}_id'.format(self_name), Integer, ForeignKey('{0}.id'.format(self_name)))
        )
        table_name = entity_name.lower()
        setattr(cls, table_name + 's',
                relationship(table_name.capitalize(), secondary=association_table,
                             backref=backref(cls.__name__.lower() + 's', lazy='dynamic')))
        return cls

    return ref_table
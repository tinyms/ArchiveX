__author__ = 'tinyms'

from tinyms.orm import Entity, Simplify, many_to_one, many_to_many
from sqlalchemy import Column, Integer, String, DateTime, Text, Date, Boolean


class Archives(Entity, Simplify):
    name = Column(String(10), nullable=False)
    alias = Column(String(10))
    sex = Column(Integer(1))
    birthday = Column(Date())
    email = Column(String(60))
    mobile_phone = Column(String(20))


@many_to_one("Archives")
class Account(Entity, Simplify):
    login_name = Column(String(20), unique=True, nullable=False)
    login_pwd = Column(String(60), nullable=False)
    enabled = Column(Boolean(), nullable=False)
    last_logon_time = Column(DateTime())
    create_time = Column(DateTime(), nullable=False)


@many_to_many("Account")
class Role(Entity, Simplify):
    name = Column(String(20), unique=True, nullable=False)
    description = Column(Text)


@many_to_many("Role")
class SecurityPoint(Entity, Simplify):
    key = Column(String(60), unique=True, nullable=False)
    description = Column(Text)
    module_name = Column(String(60), nullable=False)
    pkg_name = Column(String(60), nullable=False)


class Term(Entity, Simplify):
    name = Column(String(20), unique=True, nullable=False)
    slug = Column(String(20), nullable=False)

@many_to_one("Term")
@many_to_one("TermTaxonomy")
class TermTaxonomy(Entity, Simplify):
    taxonomy = Column(String(30), nullable=False)
    path = Column(Text, nullable=False)
    object_count = Column(Integer)
    description = Column(Text)
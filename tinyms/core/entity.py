__author__ = 'tinyms'

from sqlalchemy import Column, Integer, String, DateTime, Text, Date, Boolean, Numeric
from tinyms.core.orm import Entity, Simplify, many_to_one, many_to_many


class Archives(Entity, Simplify):
    #姓名
    name = Column(String(20), nullable=False)
    #别名、曾用名
    alias = Column(String(20))
    #性别
    sex = Column(String(5))
    #生日
    birthday = Column(Date())
    #体重(千克)
    weight = Column(Numeric(2, 2))
    #身高(厘米)
    height = Column(Numeric(2, 2))
    #民族
    nation = Column(String(65))
    #籍贯
    hometown = Column(String(10))
    #视力
    vision = Column(Numeric(2, 2))
    #职位
    post = Column(Integer())
    #健康状况
    health_state = Column(String(20))
    #婚姻状况
    marital_status = Column(Boolean())
    #身份证
    id_card = Column(String(20))
    #户籍所在地
    household_register = Column(String(100))
    #学历
    educational_background = Column(Integer())
    #专业
    specialty = Column(Integer())
    #毕业院校
    last_leave_school = Column(String(30))
    #政治面貌
    political_landscape = Column(Integer())
    #职称等级
    profession_level = Column(String(30))
    #爱好
    hobby = Column(String(60))
    #性格
    disposition = Column(String(60))
    #特长
    strong_point = Column(String(60))
    #综合技能
    comple_skills = Column(String(60))
    #现住址
    current_address = Column(String(250))
    #现住址电话
    current_address_phone = Column(String(60))
    #录用途径
    employment_pathways = Column(Integer())
    #介绍人
    employment_referrals = Column(String(10))
    #紧急联系人
    emergency_contact = Column(String(10))
    #紧急联系人电话
    emergency_contact_phone = Column(String(20))
    #邮箱
    email = Column(String(65), unique=True)
    #移动电话
    mobile_phone = Column(String(20))
    #accounts

#档案
@many_to_one("Archives")
class Account(Entity, Simplify):
    login_name = Column(String(20), unique=True, nullable=False)
    login_pwd = Column(String(60), nullable=False)
    enabled = Column(Boolean(), nullable=False)
    last_logon_time = Column(DateTime())
    create_time = Column(DateTime(), nullable=False)
    #archives
    #roles

#账户
@many_to_many("Account")
class Role(Entity, Simplify):
    name = Column(String(60), unique=True, nullable=False)
    description = Column(Text)
    #securitypoints
    #accounts

#安全点
@many_to_many("Role")
class SecurityPoint(Entity, Simplify):
    key_ = Column(String(60), unique=True, nullable=False)
    description = Column(Text)
    group_ = Column(String(60), nullable=False)
    category = Column(String(60), nullable=False)
    #roles

#职位、头衔
class JobTitle(Entity, Simplify):
    name = Column(String(60), unique=True, nullable=False)

#分类字典
class Term(Entity, Simplify):
    name = Column(String(20), unique=True, nullable=False)
    slug = Column(String(20), nullable=False)
    #termtaxonomys

#分类
@many_to_one("Term")
@many_to_one("TermTaxonomy")
class TermTaxonomy(Entity, Simplify):
    taxonomy = Column(String(30), nullable=False)
    path = Column(Text, nullable=False)
    object_count = Column(Integer)
    description = Column(Text)
    #parent
    #term
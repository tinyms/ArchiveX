__author__ = 'tinyms'

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, INET, INTEGER, INTERVAL, \
    MACADDR, NUMERIC, REAL, SMALLINT, TEXT, TIME, TIMESTAMP, \
    UUID, VARCHAR
from sqlalchemy.orm import relationship, backref, class_mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Entity = declarative_base()


def dict_json(model):
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, getattr(model, c)) for c in columns)


class User(Entity):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    odds = Column(ARRAY(Integer))
    createdate = Column(DateTime)
    posts_ = relationship("Post", order_by="Post.id", backref="users")

    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.name, self.fullname, self.createdate)


class Post(Entity):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(length=255))
    content = Column(Text)
    userid = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship("User", backref=backref('posts', order_by=id))

    def __repr__(self):
        return "<posts('%s','%s','%i')>" % (self.title, self.content, self.userid)


# engine = create_engine("postgresql+psycopg2://postgres:1@localhost/postgres", echo=True)
# Entity.metadata.create_all(engine)
# import datetime
# usr = User()
# usr.name = "JK"
# usr.fullname = "LX"
# usr.odds = [1,2,3,3,4]
# usr.createdate = datetime.datetime.now()
#
# import json
#
# Session = sessionmaker(bind=engine)
# session = Session()
# session.add(usr)
# session.commit()
# print(usr.id)
#
# for u in session.query(User).order_by(User.id):
#     items = u.posts_
#     for item in items:
#         print(json.dumps(dict_json(item)))


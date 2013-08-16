__author__ = 'tinyms'

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker

from tinyms.orm import Entity,Simplify,many_to_one,many_to_many


class User(Entity,Simplify):
    name = Column(String)
    fullname = Column(String)
    odds = Column(Integer)
    createdate = Column(DateTime)

@many_to_many("User")
class Post(Entity,Simplify):
    title = Column(String(length=255))
    content = Column(Text)

engine = create_engine("postgresql+psycopg2://postgres:1@localhost/postgres", echo=True)
Entity.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
u = User()
u.name = "Test"
session.add(u)
session.commit()
p1 = Post()
p1.title = "Odds365"
u.posts.append(p1)
session.commit()

for u in session.query(User).order_by(User.id):
    for p in u.posts:
        print(p)


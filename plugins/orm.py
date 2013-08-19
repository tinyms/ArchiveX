__author__ = 'tinyms'

from sqlalchemy import Column, Integer, String, DateTime, Text
from tinyms.orm import Entity,Simplify,many_to_one,many_to_many,SessionFactory

class User(Entity,Simplify):
    name = Column(String)
    fullname = Column(String)
    odds = Column(Integer)
    createdate = Column(DateTime)

@many_to_many("User")
class Post(Entity,Simplify):
    title = Column(String(length=255))
    content = Column(Text)

# session = SessionFactory.new()
# u = User()
# u.name = "Test"
# session.add(u)
# session.commit()
# p1 = Post()
# p1.title = "Odds365"
# u.posts.append(p1)
# session.commit()
#
# for u in session.query(User).order_by(User.id):
#     for p in u.posts:
#         print(p)


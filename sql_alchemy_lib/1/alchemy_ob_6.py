from sqlalchemy import create_engine, MetaData, Column, Integer, Table, String, ForeignKey, insert, select, update, \
    bindparam, delete, inspect
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.elements import or_


engine = create_engine(url="sqlite+pysqlite:///:memory:", echo=True)


session = Session(engine,expire_on_commit=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age : Mapped[int]

Base.metadata.create_all(engine)

user = User(id = 1, name = "Ramis", age = 20)
user1 = User(id = 2, name = "Almaz", age = 20)

insp = inspect(user)
#print(insp.transient)
session.add(user)
session.add(user1)

session_user = session.get(User,1)
print(user is session_user)
session.flush()

print(session.new)
#session.flush()
#session.delete(user)
#session.flush()
#session.commit()

#session.execute(...).scalar_one()
user_from_db = session.scalar(select(User).where(User.id ==1))
print(user_from_db is user)
user.age = 1
session.commit()
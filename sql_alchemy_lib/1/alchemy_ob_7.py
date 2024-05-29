# one to one


from sqlalchemy import create_engine, MetaData, Column, Integer, Table, String, ForeignKey, insert, select, update, \
    bindparam, delete, inspect
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.elements import or_


engine = create_engine(url="sqlite+pysqlite:///:memory:", echo=True)


session = Session(engine,expire_on_commit=True, autoflush= False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age : Mapped[int]

    address: Mapped["Address"] = relationship(back_populates="user", uselist = False)
    def __repr__(self):
        return f"User:{self.id=}:{self.name=}"



class Address(Base):
    __tablename__ = 'addresses'

    email : Mapped[str] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="address", uselist = False)
    user_fk :Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self):
        return f"Address:{self.email=}:{self.user_fk}"



Base.metadata.create_all(engine)

user = User(id = 1, name = "Ramis", age = 20)
address = Address(email = 'gcfhcjh@gmail.com')
user.address = address   # address.user = user

session.add(user)
session.commit()

users = session.scalars(select(User)).all()
addresses = session.scalars(select(Address)).all()

print(users)
print(addresses)

#user1 = User(id = 2, name = "Almaz", age = 20)

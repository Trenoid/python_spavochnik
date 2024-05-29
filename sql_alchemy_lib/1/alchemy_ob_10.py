# one to many


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

    addresses: Mapped[list["Address"]] = relationship(back_populates="user", uselist = True, lazy = "joined")

    def __repr__(self):
        return f"User:{self.id=}:{self.name=}"



class Address(Base):
    __tablename__ = 'addresses'

    email : Mapped[str] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="addresses", uselist = False)
    user_fk :Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self):
        return f"Address:{self.email=}:{self.user_fk}"



Base.metadata.create_all(engine)


user = User(id = 1, name = "Ramis", age = 20)
address = Address(email = 'gcfhcjh@gmail.com')
address2 = Address(email = 'ramistalipov90@gmail.com')
user.addresses.append(address)
user.addresses.append(address2)

session.add(user)
session.commit()


#users = session.scalars(select(User)).all()
#addresses = session.scalars(select(Address)).all()
#
#print(users)
#print(addresses)

user = session.scalar(select(User))
print(user)
print(user.addresses)
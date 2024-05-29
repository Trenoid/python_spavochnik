from sqlalchemy import create_engine, MetaData, Column, Integer, Table, String, ForeignKey, insert, select, update, \
    bindparam, delete, inspect
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.elements import or_

engine = create_engine(url="sqlite+pysqlite:///:memory:", echo=True)

session = Session(engine, expire_on_commit=True, autoflush=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)

    addresses: Mapped[list["Address"]] = relationship("Address", secondary="user_address", back_populates="users")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class Address(Base):
    __tablename__ = 'addresses'
    email: Mapped[str] = mapped_column(String, primary_key=True)

    users: Mapped[list["User"]] = relationship("User", secondary="user_address", back_populates="addresses")

    def __repr__(self):
        return f"Address(email={self.email})"


class UserAddress(Base):
    __tablename__ = "user_address"
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    address_email: Mapped[str] = mapped_column(ForeignKey('addresses.email'), primary_key=True)

    def __repr__(self):
        return f"<UserAddress(user_id={self.user_id}, address_email={self.address_email})>"


Base.metadata.create_all(engine)

user = User(id=1, name="Ramis", age=20)
user2 = User(id=2, name="Almaz", age=20)
address = Address(email='gcfhcjh@gmail.com')
address2 = Address(email='ramistalipov90@gmail.com')

user.addresses.append(address)
user.addresses.append(address2)
user2.addresses.append(address)
user2.addresses.append(address2)

session.add(user)
session.add(user2)
session.commit()

users = session.scalars(select(User)).all()
addresses = session.scalars(select(Address)).all()
user_secondary = session.scalars(select(UserAddress)).all()

print("Usersssss",users)
print(addresses)
print(user_secondary)

user = session.scalar(select(User))
print(user)
print(user.addresses)

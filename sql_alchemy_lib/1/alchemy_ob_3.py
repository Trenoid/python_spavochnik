from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, select
from sqlalchemy.orm import Session, registry, declarative_base, as_declarative, declared_attr, mapped_column, Mapped

engine = create_engine(url =  "sqlite+pysqlite:///:memory:",echo = True)

mapper_registry = registry()

#print(mapper_registry)
#print(mapper_registry.metadata)

#Base = mapper_registry.generate_base()
#Base = declarative_base()


#class AbstractModel(Base):
#    id = mapped_column(Integer, autoincrement= True , primary_key= True)

@as_declarative()
class AbstractModel:
    id : Mapped[int] = mapped_column( autoincrement= True , primary_key= True)

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__lower()


class UserModel(AbstractModel):
    __tablename__ = "users"
    user_id : Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    fullname = mapped_column(String)

class AddressModel(AbstractModel):
    __tablename__ = "addresses"
    email = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey("users.id"))


print(UserModel.__table__.__dict__)
print(AddressModel.__table__)

user = UserModel(user_id = 23, name = 'Ramis', fullname = "Ramis Talipov")

with Session(engine) as session:
    with session.begin():
        AbstractModel.metadata.create_all(engine)
        user = UserModel(user_id=23, name='Ramis', fullname="Ramis Talipov")
        session.add(user)

    with session.begin():
        res = session.execute(select(UserModel).where(UserModel.user_id ==23))
        user = res.scalar()
        user
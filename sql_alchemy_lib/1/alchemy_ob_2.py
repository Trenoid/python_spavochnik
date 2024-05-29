from sqlalchemy import create_engine, text, MetaData, Connection, Table, Column, Integer,String, BigInteger, ForeignKey
from sqlalchemy.orm import Session

engine = create_engine(url =  "sqlite+pysqlite:///:memory:",echo = True)
metadata = MetaData()


user_table = Table(
    "users",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("user_id",BigInteger,unique=True),
    Column("full_name",String),
)


address = Table(
    "addresses",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("user_id",ForeignKey('users.user_id'),),
    Column("email",String,nullable=False),
)


print(user_table.c.keys())

metadata.create_all(engine)
metadata.drop_all(engine)
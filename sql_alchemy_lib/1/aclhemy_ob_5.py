from sqlalchemy import create_engine, MetaData, Column, Integer, Table, String, ForeignKey, insert, select, update, \
    bindparam, delete
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.sql.elements import or_


engine = create_engine(url="sqlite+pysqlite:///:memory:", echo=True)

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id",Integer, primary_key= True,unique= True,autoincrement=True),
    Column("name", String(30),),
    Column("second_name",String(30),),
)

address = Table(
    "addresses",
    metadata,
    Column("id",Integer,primary_key=True,unique=True, autoincrement=True),
    Column("user_id",ForeignKey('users.id'),),
    Column("email_address",String(30)),
)

metadata.create_all(engine)

stmt = insert(user_table).values(name = "test", second_name = "test")
stmt_wo_values = insert(user_table)
#postgresql_stmt = stmt.compile(engine,postgresql.dialect())
#sqlite_stmt = stmt.compile(engine,sqlite.dialect())

postgresql_stmt = stmt_wo_values.compile(engine,postgresql.dialect())
sqlite_stmt = stmt_wo_values.compile(engine,sqlite.dialect())

print(sqlite_stmt.params)
print(postgresql_stmt.params)

#with engine.begin() as conn:
#    result = conn.execute(sqlite_stmt)
#    print(result.inserted_primary_key)

with engine.begin() as conn:
    conn.execute(stmt_wo_values,
                            [
                              {"name" : "Test1", "second_name": "Test1 Full"},
                              {"name" : "Test2", "second_name": "Test2 Full"},
                              {"name" : "Test3", "second_name": "Test3 Full"},
                            ]
                         )

    conn.execute(
        insert(address),
                          [
                              {"user_id": 1, "email_address": "Test1@gmail.com"},
                              {"user_id": 2, "email_address": "Test2@gmail.com"},
                              {"user_id": 3, "email_address": "Test3@gmail.com"},
                          ]
                          )

#with engine.begin() as conn:
#    conn.execute(
#        update(user_table).where(user_table.c.id ==1).values(name = "Updated name 1")
#    )
#
#    print(conn.execute(select(user_table).where(user_table.c.id ==1)).all())


#with engine.begin() as conn:
#    stmt = update(user_table).where(user_table.c.name == bindparam("oldname")).values(name =bindparam("newname"))
#
#    conn.execute(
#        stmt,
#        [
#            {"oldname": "Test1", "newname": "NewTest1"},
#            {"oldname": "Test2", "newname": "NewTest2"},
#            {"oldname": "Test3", "newname": "NewTest3"},
#        ]
#    )
#    print(conn.execute(select(user_table)).all())


#with engine.begin() as conn:
#
#    conn.execute(
#    delete(user_table).where(user_table.c.id ==1)
#    )
#    print(conn.execute(select(user_table)).all())


with engine.begin() as conn:
    delete_stmt = (
        delete(user_table)
        .where(user_table.c.id == address.c.user_id)
        .where(address.c.email_address == "Test1@gmail.com" )
    )


    print(delete_stmt.compile(dialect=postgresql.dialect()))
    print(delete_stmt.compile(dialect=postgresql.dialect()))
    print(conn.execute(select(user_table)).all())

with engine.begin() as conn:

    delete_stmt = (
        delete(user_table)
        .where(user_table.c.id ==1)
        .returning(user_table.c.id)
    )

    #result = conn.execute(select(user_table))
    #print("Deleted",result.rowcount)

    result = conn.execute(delete_stmt).all()
    print("del",result)

from sqlalchemy import create_engine, MetaData, Column, Integer, Table, String, ForeignKey, insert, select
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

with engine.begin() as conn:
    result = conn.execute(
        select(user_table).where(user_table.c.name == "Test1")
    )
    print(result.all())

    result = conn.execute(
        select(user_table).where(user_table.c.name.startswith("Test"),
                                 user_table.c.name.contains("2")
        )
    )
    print(result.all())

    result = conn.execute(
        select(user_table.c.name, user_table.c.id).where(or_(user_table.c.name.startswith("Test2"),
                                 user_table.c.name.contains("3"))
                                 )
    )
    print(result.all())

    result = conn.execute(
        select(
            (user_table.c.name + ' ' + user_table.c.second_name).label("fullname")
               ).where(
            user_table.c.id.in_([1,2])
        )
    )
    #for res in result:
    #    print(res.fullname)
    print(result.mappings().all())

    result = conn.execute(
        select(
            address.c.email_address.label("email"),
            (user_table.c.name + ' ' + user_table.c.second_name).label("fullname")
        ).where(
            user_table.c.id > 1
        ).join_from(user_table,address, user_table.c.id == address.c.user_id)    #).join(address)
        .order_by(
            user_table.c.id.desc()
        ).group_by(
            "email"
        ).having(

        )
    )

    print(result.all())
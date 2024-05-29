from sqlalchemy import create_engine, text

engine = create_engine(url = "sqlite+pysqlite:///:memory:",echo = True)

with engine.connect() as connection:
    result = connection.execute(text("select 'Hello, world!' "))
    #print(result.all())
    result = connection.execute(text("select 'Hello, world!' "))
    #print(result.scalar())
    result = connection.execute(text("select 'Hello, world!' "))
    print(result.scalars())
    result = connection.execute(text("select 'Hello, world!' "))
    print(result.scalars().all())

    result = connection.execute(text("select 'Hello, world!' "))
    print(result.scalar_one_or_none())
    #print(result.scalars().one_or_none())
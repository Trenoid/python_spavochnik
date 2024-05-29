import asyncio
import os
import sys

# Добавление родительского каталога в sys.path для доступа к модулям
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.orm import create_tables, insert_data, async_insert_data


def main():
    # Создание таблиц
    create_tables()

    # Вставка данных в синхронном режиме
    insert_data()

    # Вставка данных в асинхронном режиме
    asyncio.run(async_insert_data())


if __name__ == "__main__":
    main()

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# 1. Загружаем переменные окружения
load_dotenv()

# 2. Объект конфигурации Alembic
config = context.config

# 3. Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Устанавливаем URL базы из .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# 5. Импорт метаданных твоих моделей для автогенерации
# Убедись, что путь 'app.models.endpointer_models' верный
from app.models.endpointer_models import Base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """Вспомогательная функция для запуска миграций в синхронном контексте."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Создание асинхронного движка и запуск миграций."""
    
    # Получаем секцию настроек (обычно это [alembic])
    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        configuration = {}

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Используем run_sync для запуска синхронного Alembic в асинхронном соединении
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме."""
    # Запускаем асинхронный цикл событий
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

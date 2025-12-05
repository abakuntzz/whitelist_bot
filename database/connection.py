from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from pathlib import Path

secret_path = Path(__file__).parent.parent / "secrets" / "db_secret.txt"

if not secret_path.exists():
    # Создаем файл если его нет
    secret_path.parent.mkdir(exist_ok=True)
    with open(secret_path, 'w') as f:
        f.write("sqlite+aiosqlite:///whitelist.db")

with open(secret_path, 'r') as f:
    lines = f.readlines()

db_url = None
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        db_url = line
        break

if not db_url:
    db_url = "sqlite+aiosqlite:///whitelist.db"

# Создаем подключение к SQLite
engine = create_async_engine(db_url, echo=False)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    """Получить сессию БД"""
    async with AsyncSessionLocal() as session:
        yield session

# Функция для создания таблиц
async def create_tables():
    """Создать таблицы если их нет"""
    from .models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы созданы/проверены")

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    async_sessionmaker
from pathlib import Path

secret_path = Path(__file__).parent.parent / "secrets" / "db_secret.txt"

if not secret_path.exists():
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

engine = create_async_engine(db_url, echo=False)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    from .bd_structure import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

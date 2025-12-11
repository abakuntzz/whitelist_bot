from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from pathlib import Path

def get_url() -> str:
    secret_path = Path(__file__).parent.parent / "secrets" / "db_secret.txt"
    with open(secret_path, 'r') as f:
        url = f.read().strip()
        return url
  
db_url = get_url()
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

from sqlalchemy import Column, Integer, String, Boolean, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# setup base
Base = declarative_base()

# task table model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)

# setup config database
DB_URL = "sqlite+aiosqlite:///tasks_management.db"
engine = create_async_engine(DB_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
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

async def init_db(custom_engine=None):
    """database init and make table"""
    target_engine = custom_engine or engine
    async with target_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_task_db(description: str, custom_session=None) -> int:
    """add new task to database"""
    session_factory = custom_session or AsyncSessionLocal
    async with session_factory() as session:
        new_task = Task(description=description)
        session.add(new_task)
        await session.commit()
        return new_task.id

async def get_all_tasks_db(custom_session=None):
    """get all task list"""
    session_factory = custom_session or AsyncSessionLocal
    async with session_factory() as session:
        result = await session.execute(select(Task))
        return result.scalars().all()

async def delete_task_db(task_id: int, custom_session=None) -> bool:
    """remove task based on id"""
    session_factory = custom_session or AsyncSessionLocal
    async with session_factory() as session:
        task = await session.get(Task, task_id)
        if task:
            await session.delete(task)
            await session.commit()
            return True
        return False
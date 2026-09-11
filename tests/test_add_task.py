import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import database


@pytest.mark.asyncio
async def test_add_task():
    # setup temporary database for testing
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    await database.init_db(test_engine)
    TestSession = async_sessionmaker(test_engine, expire_on_commit=False)

    # execute add_task_db function
    task_id = await database.add_task_db("Belajar SQLAlchemy", TestSession)

    # verified return id
    assert task_id == 1

    # verified data put into database
    tasks = await database.get_all_tasks_db(TestSession)
    assert len(tasks) == 1
    assert tasks[0].description == "Belajar SQLAlchemy"
    assert tasks[0].is_completed is False
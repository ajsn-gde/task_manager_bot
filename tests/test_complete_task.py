import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import database


@pytest.mark.asyncio
async def test_complete_task_success():
    # setup db
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    await database.init_db(test_engine)
    TestSession = async_sessionmaker(test_engine, expire_on_commit=False)

    # add new task
    task_id = await database.add_task_db("Belajar Asyncio", TestSession)

    # mark task as completed
    is_updated = await database.complete_task_db(task_id, TestSession)

    # verify return value and status in database
    assert is_updated is True

    tasks = await database.get_all_tasks_db(TestSession)
    assert len(tasks) == 1
    assert tasks[0].is_completed is True
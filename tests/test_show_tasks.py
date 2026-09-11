import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import database

@pytest.mark.asyncio
async def test_get_all_tasks_with_data():
    # setup db
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    await database.init_db(test_engine)
    TestSession = async_sessionmaker(test_engine, expire_on_commit=False)

    # add some dummy data
    await database.add_task_db("Tugas 1", TestSession)
    await database.add_task_db("Tugas 2", TestSession)

    # get all task
    tasks = await database.get_all_tasks_db(TestSession)

    # verify the total and description
    assert len(tasks) == 2
    assert tasks[0].description == "Tugas 1"
    assert tasks[1].description == "Tugas 2"

@pytest.mark.asyncio
async def test_get_all_tasks_empty():
    # setup db
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    await database.init_db(test_engine)
    TestSession = async_sessionmaker(test_engine, expire_on_commit=False)

    # take task when db is empty
    tasks = await database.get_all_tasks_db(TestSession)

    # verify result must be empty list
    assert len(tasks) == 0
    assert tasks == []
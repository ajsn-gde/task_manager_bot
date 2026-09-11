import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import database


@pytest.mark.asyncio
async def test_delete_task_success():
    # setup db
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    await database.init_db(test_engine)
    TestSession = async_sessionmaker(test_engine, expire_on_commit=False)

    # add dummy data
    task_id = await database.add_task_db("Tugas yang akan dihapus", TestSession)

    # remove task 
    is_deleted = await database.delete_task_db(task_id, TestSession)

    # verify the task already deleted
    assert is_deleted is True

    # make sure data is not in db again
    tasks = await database.get_all_tasks_db(TestSession)
    assert len(tasks) == 0


@pytest.mark.asyncio
async def test_delete_task_not_found():
    # setup
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    await database.init_db(test_engine)
    TestSession = async_sessionmaker(test_engine, expire_on_commit=False)

    # remove not found id (ID: 999)
    is_deleted = await database.delete_task_db(999, TestSession)

    # must be return false because the id is not found in db
    assert is_deleted is False
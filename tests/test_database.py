from asyncio import TimeoutError
import pytest
from asyncpg.exceptions import StringDataRightTruncationError
from toolbox import DBPool
from .conftest import db_config

pytestmark = [pytest.mark.asyncio]


@pytest.fixture
async def tmp_table(db):
    await db.execute('create table tmp_table (id int, message varchar(4))')
    yield
    await db.execute('drop table tmp_table')


async def test_fetch(db):
    query = 'select * from unnest(array[1, 2]) col'
    records = await db.fetch(query)

    assert len(records) == 2
    for row in records:
        assert isinstance(row['col'], int)


async def test_fetch_with_args(db):
    query = 'select * from unnest(array[1, 2]) col where col = $1'
    result = await db.fetchval(query, 2)

    assert result == 2


async def test_fetch_none(db):
    query = 'select * from unnest(array[1, 2]) col where col = $1'
    result = await db.fetchval(query, 3)

    assert result is None


async def test_fetchrow(db):
    query = 'select * from unnest(array[1, 2]) col'
    records = await db.fetchrow(query)

    assert len(records) == 1


async def test_fetchval(db):
    assert await db.fetchval('select 1') == 1


async def test_execute(db):
    assert await db.execute('select current_date')


async def test_executemany(db, tmp_table):
    query = 'insert into tmp_table values ($1, $2)'
    data = [(idx, 'test') for idx in range(10)]

    assert await db.executemany(query, data) is None
    assert await db.fetchval('select count(*) from tmp_table') == 10


async def test_executemany_empty(db, tmp_table):
    query = 'insert into tmp_table values ($1, $2)'

    assert await db.executemany(query, ()) is None
    assert await db.fetchval('select count(*) from tmp_table') == 0


async def test_timeout(db):
    with pytest.raises(TimeoutError):
        assert await db.fetchval('select pg_sleep(2)', timeout=1)


async def test_transaction_rollback(db, tmp_table):
    query = 'insert into tmp_table values ($1, $2)'
    data = [(1, 'test'), (2, 'megatest')]

    with pytest.raises(StringDataRightTruncationError):
        assert await db.executemany(query, data)
    assert await db.fetchval('select count(*) from tmp_table') == 0


async def test_codecs():
    db = DBPool(db_config)
    db.set_codec('int4', encoder=lambda v: v, decoder=str)
    db.set_codec('varchar', encoder=lambda v: v, decoder=int)
    await db.create()

    assert await db.fetchval("select 1::integer") == '1'
    assert await db.fetchval("select '1'::varchar") == 1

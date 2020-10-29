import asyncio
import asyncpg
from datetime import datetime
from starlette.responses import JSONResponse, PlainTextResponse
import nest_asyncio


nest_asyncio.apply()

async def db_setup():
    global conn_pool
    conn_pool = await asyncpg.create_pool(
                database='tester',
                port = 5432)


conn_pool = None
loop = asyncio.get_event_loop()
loop.run_until_complete(db_setup())


async def create_notes_query(title, content):
    date = datetime.now()
    async with conn_pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO notes(title, content, date_created) VALUES($1, $2, $3)
            ''', title, content, date)


# needs refactor to serialize the record obj.
async def all_notes_query(request):
    async with conn_pool.acquire() as connection:
        data = await connection.fetch('select * from notes')
        length = len(data)
        records = {}
        for i in range(length):
            records[i] = str(data[i])
    
    return JSONResponse(records)




import asyncio
import asyncpg
from datetime import datetime
from starlette.responses import JSONResponse
import nest_asyncio
from typing import List, Dict


# Nesting the event loop.
nest_asyncio.apply()


# DB Setup
async def db_setup():
    global conn_pool
    conn_pool = await asyncpg.create_pool(
                database='tester',
                port=5432)


conn_pool = None
loop = asyncio.get_event_loop()
loop.run_until_complete(db_setup())


# Creates note
async def create_notes_query(title: str, content: str):
    date = datetime.now()
    async with conn_pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO notes(title, content, date_created) VALUES($1, $2, $3)
            ''', title, content, date)


# Returns JSON responsse of note objects
async def all_notes_query(request):
    async with conn_pool.acquire() as connection:
        data = await connection.fetch('select * from notes')
        length: int = len(data)
        records: Dict = {}
        result: List = []
        for i in range(length):
            record = data[i]
            uid = record['id']
            title = record['title']
            content = record['content']
            date_created = record['date_created']

            records = {
                "id": uid,
                "title": title,
                "content": content,
                "date_created": str(date_created)
            }
            result.append(records)
            records = {}
    return JSONResponse(result)


# Return DEL 1 or 0 as a result, 1 if deleted and 0 if not.
async def del_note(note_id: int):
    async with conn_pool.acquire() as connection:
        result = await connection.execute('''
            DELETE FROM notes WHERE id= $1''', note_id)
        return result


# Edit note
async def edit_notes(note_id: int, title: str, content: str):
    update_date = datetime.now()
    async with conn_pool.acquire() as connection:
        if title != "" and content != "":
            result = await connection.execute('''UPDATE notes SET title = $1, content = $2,
                                date_created = $3 WHERE id = $4
                                ''', title, content, update_date, note_id)

        elif title == "":
            result = await connection.execute('''UPDATE notes SET content = $1,
                                date_created = $2 WHERE id = $3
                                ''', content, update_date, note_id)

        elif content == "":
            result = await connection.execute('''UPDATE notes SET title = $1,
                                date_created = $2 WHERE id = $3
                                ''', title, update_date, note_id)
        else:
            result = ['Cannot write with empty data']
        return result


# Returns a note with specific ID
async def note(note_id: int):
    async with conn_pool.acquire() as connection:
        record = await connection.fetch('''
                        SELECT * FROM notes WHERE id=$1''', note_id)

        record = record[0]

        uid: int = int(record['id'])
        title: str = record['title']
        content: str = record['content']
        date_created: str = str(record['date_created'])

        result = {
            "id": uid,
            "title": title,
            "content": content,
            "date_created": date_created
        }
    return JSONResponse(result)

# End points for the API
# Imports
from starlette.responses import JSONResponse, PlainTextResponse
from db import create_notes_query, all_notes_query, del_note, edit_notes, note
import asyncio


# root
async def root(request):
    return JSONResponse({"ms": "Welcome to Notes app."})


# create note
async def create_note(request):
    data = await request.json()
    title = data["title"]
    content = data["content"]
    await create_notes_query(title,content)
    return PlainTextResponse("Note created")


# edit note
async def edit_note(request):
    _id: int = int(request.path_params['note_id'])
    data = await request.json()
    _content: str = ""
    _title: str = ""

    # get content if it is provided
    try:
        _content = data["content"]
    except:
        _content = ""

    # get title if it is provided
    try:
        _title = data["title"]
    except:
        _title = ""

    result: str = await edit_notes(note_id = _id, content = _content, title = _title)
    return PlainTextResponse(result)


# delete note
async def delete_note(request):
    note_id: int = int(request.path_params['note_id'])
    result = await del_note(note_id)
    return PlainTextResponse(str(result))

    

async def all_notes(request):
    data = await all_notes_query(request)
    return data

async def note_by_id(request):
        _id : int = int(request.path_params['note_id'])

        result = await note(note_id = int(_id))

        return result
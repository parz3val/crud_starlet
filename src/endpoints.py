# End points for the API
# Imports
from starlette.responses import JSONResponse, PlainTextResponse
from db import create_notes_query, all_notes_query
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
    return PlainTextResponse("Note edited.")


# delete note
async def delete_note(request):
    return PlainTextResponse("Note deleted!")

async def all_notes(request):
    data = await all_notes_query(request)
    return data




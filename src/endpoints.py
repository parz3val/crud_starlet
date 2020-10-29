# End points for the API
# Imports
from starlette.responses import JSONResponse, PlainTextResponse


# root
async def root(request):
    return JSONResponse({"ms": "Welcome to Notes app."})


# create note
async def create_note(request):
    return PlainTextResponse("Note created")


# edit note
async def edit_note(request):
    return PlainTextResponse("Note edited.")


# delete note
async def delete_note(request):
    return PlainTextResponse("Note deleted!")

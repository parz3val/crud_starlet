# Imports

from starlette.applications import Starlette as st
from starlette.routing import Route
from endpoints import root, create_note, edit_note, delete_note, all_notes, note_by_id




# Contains the routes for the app.
routes = [
    Route("/", endpoint = root),
    Route("/all",endpoint = all_notes),
    Route("/create", endpoint = create_note, methods = ["POST"]),
    Route("/edit_note/{note_id}", edit_note, methods = ["POST"]),
    Route("/delete_note/{note_id}", delete_note, methods = ["POST"]),
    Route("/note/{note_id}", note_by_id, methods = ["GET"])
        
]

app = st(debug=True, routes=routes)

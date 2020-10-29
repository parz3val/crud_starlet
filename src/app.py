# Imports

from starlette.applications import Starlette as st
from starlette.routing import Route
from endpoints import root, create_note, edit_note, delete_note


# Contains the routes for the app.
routes = [
    Route("/", root),
    Route("/create", create_note),
    Route("/edit_note/{note_id}", edit_note),
    Route("/delete_note/{note_id}", delete_note),
]

app = st(debug=True, routes=routes)

import os

from starlette.applications import Starlette

from .db import close_db, database, init_db
from .routes import api_routes

DEBUG = os.environ.get('DEBUG', 'true')
if DEBUG == 'true':
    DEBUG == True
else:
    DEBUG == False

app = Starlette(debug=DEBUG, routes=api_routes, on_startup=[init_db], on_shutdown=[close_db],)

app.state.database = database

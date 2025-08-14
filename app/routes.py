from app import app, db
from app.routers.Flow import *
from app.routers.Task import *
from app.routers.Perosn import *
from app.routers.Invite import *
from app.routers.Team import *

@app.route('/')
def index():
    return ("Welcome")
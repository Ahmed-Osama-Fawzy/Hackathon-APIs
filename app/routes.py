from app import app, db
from app.routers.Flow import *
from app.routers.Task import *
# from app.routers.Course import *

@app.route('/')
def index():
    return ("Welcome")
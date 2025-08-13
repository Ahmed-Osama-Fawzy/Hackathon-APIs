from app import app, db
from app.routers.Flow import *
# from app.routers.Account import *
# from app.routers.Course import *

@app.route('/')
def index():
    return ("Welcome")
import configs as _
import init
from init.api import app


@app.on_event('startup')
def startup():
    init.startup()


@app.on_event('shutdown')
def shutdown():
    init.shutdown()

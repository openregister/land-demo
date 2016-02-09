import os
from land.factory import create_app
app = create_app(os.environ['SETTINGS'])

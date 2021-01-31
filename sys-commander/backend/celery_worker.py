#!/usr/bin/env python3
import os
from backend.app import app_celerey, create_app
from flask.logging import default_handler

from dotenv import load_dotenv
load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()


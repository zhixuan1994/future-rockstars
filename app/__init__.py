import json
import os
from flask import Flask
from tinydb import TinyDB, Query

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
app = Flask(
    __name__,
    static_folder=os.path.join(CUR_DIR, 'static'),
    template_folder=os.path.join(CUR_DIR, 'templates'))
app.config.update(
    DEBUG=True
)

# Initialize the database with boilerplate JSON
db = TinyDB('../db.json')
db.purge()
with open('./data/bands.json') as bands_data:
    bands = json.load(bands_data)
    db.insert_multiple(bands)
with open('./data/members.json') as members_data:
    members = json.load(members_data)
    db.insert_multiple(members)
with open('./data/dorms.json') as dorms_data:
    dorms = json.load(dorms_data)
    db.insert_multiple(dorms)

app = Flask(__name__)

from app import views

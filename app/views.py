from app import app
from flask import render_template
from tinydb import TinyDB, Query

db = TinyDB('../db.json')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def indexView():
    return render_template('index.html', title='Home')

@app.route('/bands', methods=['GET'])
def bandsView():
    return render_template('bands.html', title='Bands')

@app.route('/dorms', methods=['GET'])
def dormsView():
    return render_template('dorms.html', title='Dorms')

@app.route('/members', methods=['GET'])
def membersView():
    Entry = Query()
    members = db.search(Entry.type == 'member')
    return render_template('members.html', title='Members', members=members)

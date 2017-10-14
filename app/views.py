from app import app
from flask import redirect, render_template, request
from tinydb import TinyDB, Query

db = TinyDB('../db.json')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def indexView():
    return render_template('index.html', title='Home')

@app.route('/bands', methods=['GET'])
def bandsView():
    Entry = Query()
    bands = db.search(Entry.type == 'band')
    return render_template('bands.html', title='Bands', bands=bands)

@app.route('/dorms', methods=['GET'])
def dormsView():
    Entry = Query()
    dorms = db.search(Entry.type == 'dorm')
    return render_template('dorms.html', title='Dorms', dorms=dorms)

@app.route('/members', methods=['GET'])
def membersView():
    Entry = Query()
    members = db.search(Entry.type == 'member')
    return render_template('members.html', title='Members', members=members)

@app.route('/members/add', methods=['POST'])
def addMember():
    member_name = request.form.getlist('name')[0]
    member_age = request.form.getlist('age')[0]
    member_gender = request.form.getlist('gender')[0]
    member_talent = request.form.getlist('talent')[0]
    db.insert({'type': 'member', 'name': member_name, 'gender': member_gender, 'age': member_age, 'talent': member_talent, 'status': 'Pending', 'checkin': False})
    return redirect('/members')

@app.route('/members/delete', methods=['POST'])
def deleteMember():
    member_name = request.form.getlist('name')[0]
    Member = Query()
    db.remove(Member.name == member_name)
    return redirect('/members')

@app.route('/members/checkout', methods=['POST'])
def checkOutMember():
    member_name = request.form.getlist('name')[0]
    Member = Query()
    db.update({'checkin': False}, Member.name == member_name)
    return redirect('/members')

@app.route('/members/checkin', methods=['POST'])
def checkInMember():
    member_name = request.form.getlist('name')[0]
    Member = Query()
    db.update({'checkin': True}, Member.name == member_name)
    return redirect('/members')

@app.route('/members/edit', methods=['POST'])
def editMember():
    member_name = request.form.getlist('name')[0]
    Member = Query()
    member = db.search(Member.name == member_name)
    return render_template('edit-member.html', title='Edit Member', member=member[0])

@app.route('/members/update', methods=['POST'])
def updateMember():
    member_age = request.form.getlist('age')[0]
    member_gender = request.form.getlist('gender')[0]
    member_talent = request.form.getlist('talent')[0]
    Member = Query()
    db.update({'name': member_name, 'gender': member_gender, 'age': member_age, 'talent': member_talent}, Member.name == member_name)
    return redirect('/members')

@app.route('/email', methods=['POST'])
def sendEmail():
    return render_template('email.html')

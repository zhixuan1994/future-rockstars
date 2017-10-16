from app import app
from flask import render_template, redirect, request
from random import *
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
    member_id = randint(50, 500)
    member_firstName = request.form.getlist('firstName')[0]
    member_lastName = request.form.getlist('lastName')[0]
    member_gender = request.form.getlist('gender')[0]
    member_age = request.form.getlist('age')[0]
    member_street = request.form.getlist('street')[0]
    member_city = request.form.getlist('city')[0]
    member_state = request.form.getlist('state')[0]
    member_zipCode = request.form.getlist('zipCode')[0]
    member_talent = request.form.getlist('talent')[0]
    db.insert({
        'memberId': member_id,
        'type': 'member', 
        'firstName': member_firstName,
        'lastName': member_lastName, 
        'gender': member_gender, 
        'age': member_age, 
        'street': member_street, 
        'city': member_city,
        'state': member_state,
        'zipCode': member_zipCode,
        'talent': member_talent,
        'status': 'Pending',
        'checkin': False,
        'forms': False,
        'payment': False
    })
    return redirect('/members')

@app.route('/members/delete', methods=['POST'])
def deleteMember():
    member_id = request.form.getlist('memberId')[0]
    Member = Query()
    db.remove(Member.memberId == member_id)
    return redirect('/members')

@app.route('/members/checkout', methods=['POST'])
def checkOutMember():
    member_id = request.form.getlist('memberId')[0]
    Member = Query()
    db.update({'checkin': False}, Member.memberId == member_id)
    return redirect('/members')

@app.route('/members/checkin', methods=['POST'])
def checkInMember():
    member_id = request.form.getlist('memberId')[0]
    Member = Query()
    db.update({'checkin': True}, Member.memberId == member_id)
    return redirect('/members')

@app.route('/members/edit', methods=['POST'])
def editMember():
    member_id = request.form.getlist('memberId')[0]
    Member = Query()
    member = db.search(Member.memberId == member_id)
    return render_template('edit-member.html', title='Edit Member', member=member[0])

@app.route('/members/update', methods=['POST'])
def updateMember():
    member_id = request.form.getlist('memberId')[0]
    member_gender = request.form.getlist('gender')[0]
    member_age = request.form.getlist('age')[0]
    member_street = request.form.getlist('street')[0]
    member_city = request.form.getlist('city')[0]
    member_state = request.form.getlist('state')[0]
    member_zipCode = request.form.getlist('zipCode')[0]
    member_talent = request.form.getlist('talent')[0]
    member_status = request.form.getlist('status')[0]
    member_checkin = request.form.getlist('checkin')[0]
    member_forms = request.form.getlist('forms')[0]
    member_payment = request.forms.getlist('payment')[0]
    Member = Query()
    db.update({
        'gender': member_gender, 
        'age': member_age, 
        'street': member_street, 
        'city': member_city, 
        'state': member_state, 
        'zipCode': member_zipCode, 
        'talent': member_talent, 
        'status': member_status,
        'checkin': member_checkin,
        'forms': member_forms,
        'payment': member_payment
    }, Member.memberId == member_id)
    return redirect('/members')

@app.route('/email/send', methods=['POST'])
def sendEmail():
    member_id = request.form.getlist('memberId')[0]
    email_type = request.form.getlist('type')[0]
    Member = Query()
    member = db.search(Member.memberId == member_id)
    return render_template('email.html', title="Email Template", type=email_type, member=member[0])

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
    rawBands = db.search(Entry.type == 'band')
    bands = []
    
    for b in rawBands:
        band = dict(b)
        band['name'] = band['name'].split()
        band['name'] = 'Band ' + str(int(band['name'][1]) + 1)
        band['singer'] = band['singer'].split()
        band['singer'] = band['singer'][1] + ' ' + band['singer'][2]
        band['guitarist'] = band['guitarist'].split()
        band['guitarist'] = band['guitarist'][1] + ' ' + band['guitarist'][2]
        band['drummer'] = band['drummer'].split()
        band['drummer'] = band['drummer'][1] + ' ' + band['drummer'][2]
        band['bassist'] = band['bassist'].split()
        band['bassist'] = band['bassist'][1] + ' ' + band['bassist'][2]
        band['keyboardist'] = band['keyboardist'].split()
        band['keyboardist'] = band['keyboardist'][1] + ' ' + band['keyboardist'][2]
        band['instrumentalist'] = band['instrumentalist'].split()
        band['instrumentalist'] = band['instrumentalist'][1] + ' ' + band['instrumentalist'][2]
        bands.append(band)

    return render_template('bands.html', title='Bands', bands=bands)

@app.route('/dorms', methods=['GET'])
def dormsView():
    Entry = Query()
    rawDorms = db.search(Entry.type == 'dorm')
    dorms = []

    for d in rawDorms:
        dorm = dict(d)
        dorm['name'] = dorm['name'].split()
        dorm['name'] = 'Dorm ' + str(int(dorm['name'][1]) + 1)
        if dorm['gender'] == 'male':
            dorm['gender'] == 'Male'
        else:
            dorm['gender'] == 'Female'
        for i, m in enumerate(dorm['members']):
            member = dorm['members'][i].split()
            member = member[1] + ' ' + member[2]
            dorm['members'][i] = member
        dorms.append(dorm)
    
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
    member_comments = request.forms.getlist('comments')[0]
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
        'payment': member_payment,
        'comments': member_comments
    }, Member.memberId == member_id)
    return redirect('/members')

@app.route('/email/send', methods=['POST'])
def sendEmail():
    member_id = request.form.getlist('memberId')[0]
    email_type = request.form.getlist('type')[0]
    Member = Query()
    member = db.search(Member.memberId == member_id)
    return render_template('email.html', title="Email Template", type=email_type, member=member[0])

# Custom error handling
@app.errorhandler(404)
def notFoundError(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internalError(error):
    return render_template('500.html'), 500

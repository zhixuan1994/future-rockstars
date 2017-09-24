from app import app
from flask import render_template

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def indexView():
    return render_template('index.html', title='Home')

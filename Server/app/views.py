from flask import render_template
from flask import jsonify
from flask import request
from flask import json
from flask import Response
from models import User, Bank
from app import app
from database import db_session
import datetime
import time
import json

def as_dict(model_obj):
    k = {}
    for c in model_obj.__table__.columns:
        val = getattr(model_obj, c.name)
        if isinstance(val, datetime.time):
            val = val.strftime('%H:%M:%S')
        k[c.name] = val
    return k

@app.route('/addBank', methods = ['POST'])
def addBank():
    params = ['name', 'locality', 'city', 'ifsc_code', 'start_time', 'end_time', 'password', 'username']
    for param in params:
        if request.form.get(param) is None:
            return Response(param + ' field is required', status=400)

    bank = Bank.query.filter_by(ifsc_code=request.form['ifsc_code']).first()
    if bank is not None:
        return Response('Bank with the same ifsc code already exists', status=400)

    bank = Bank.query.filter_by(username=request.form['username']).first()
    if bank is not None:
        return Response('Bank with the same username already exists', status=400)

    bank = Bank(name=request.form['name'], locality=request.form['locality'], 
        city=request.form['city'], start_time=request.form['start_time'], end_time=request.form['end_time'],
        ifsc_code=request.form['ifsc_code'], password=request.form['password'], username=request.form['username'])

    session = db_session()
    session.add(bank)
    session.commit()

    bank_json = as_dict(bank)
    return Response(json.dumps(bank_json), status=200)

@app.route('/login', methods = ['POST'])
def login():
    if request.form.get('username') is None:
        return Response(' username field is required', status=400)
    if request.form.get('password') is None:
        return Response('password field is required', status=400)
    
    bank = Bank.query.filter_by(username=request.form['username']).first()
    if bank is None: 
        return Response('Username doesnot exists', status=400)
    else:
        if not bank.check_password(request.form['password']):
            return Response('Please enter correct password', status=400)

    return Response('logged in successfully', status=200)

@app.route('/getBankDetails', methods = ['GET'])
def bankDetails():
    bank = Bank.query.filter_by(username=request.args.get('username')).first()
    bank_json = as_dict(bank)

    return Response(json.dumps(bank_json), status=200)






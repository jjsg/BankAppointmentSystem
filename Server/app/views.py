from flask import render_template
from flask import jsonify
from flask import request
from flask import json
from models import User, Bank
from app import app
from database import db_session

@app.route('/add', methods = ['POST'])
def addUser():
   return "rishabh"


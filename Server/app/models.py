from sqlalchemy import Column, Integer, String, TIME, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class Bank(Base):
    __tablename__ = 'bank'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable = False)
    locality = Column(String(100), nullable = False)
    city = Column(String(50), nullable = False)
    start_time = Column(TIME(), nullable = False)
    end_time = Column(TIME(), nullable = False)
    ifsc_code = Column(String(50), unique=True)
    password = Column(String(100), nullable = False)
    username = Column(String(50), unique=True)

    ifsc = relationship('User', backref="bank")

    def __init__(self, name=None, locality=None, city=None, start_time=None, end_time=None, 
        ifsc_code=None, password=None, username=None):
        self.name = name
        self.locality = locality
        self.city = city
        self.start_time = start_time
        self.end_time = end_time
        self.ifsc_code = ifsc_code
        self.set_password(password)
        self.username = username

    def __repr__(self):
        return '<Bank %r>' % (self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable = False)
    time = Column(TIME(), nullable = False)
    appointment_id = Column(String(10), unique=True)
    bank_ifsc_code = Column(String(50), ForeignKey('bank.ifsc_code'), nullable=False)

    def __init__(self, name=None, time=None, appointment_id=None, bank_ifsc_code=None):
        self.name = name
        self.time = time
        self.appointment_id = appointment_id
        self.bank_ifsc_code = bank_ifsc_code

    def __repr__(self):
        return '<User %r>' % (self.name)

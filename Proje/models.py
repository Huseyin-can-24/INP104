from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

# Veritabanı nesnesini oluştur
db = SQLAlchemy()

# User modeli
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    medical_history = db.Column(db.Text)

    user = db.relationship('User', backref='patient', uselist=False)
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')
    symptoms = db.relationship('Symptom', backref='patient', lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id
        user = User.query.get(user_id)
        if user:
            self.full_name = user.full_name

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))

    user = db.relationship('User', backref='doctor', uselist=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')

    def __init__(self, user_id, specialization=None):
        self.user_id = user_id
        self.specialization = specialization
        user = User.query.get(user_id)
        if user:
            self.full_name = f"Dr. {user.full_name}"

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    fever = db.Column(db.Boolean, default=False)
    fever_temperature = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'cancelled'

    prescription = db.relationship('Prescription', backref='appointment', uselist=False)

    def __init__(self, patient_id, doctor_id, date_time, reason, status='pending'):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_time = date_time
        self.reason = reason
        self.status = status

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    medications = db.Column(db.Text)
    instructions = db.Column(db.Text)
    issue_date = db.Column(db.Date, default=date.today)
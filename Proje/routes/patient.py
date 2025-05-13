
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Patient, Appointment
from flask import  redirect, url_for, flash
from models import Doctor
from forms import AppointmentForm
from datetime import datetime

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).all() if patient else []
    return render_template('patient/dashboard.html', appointments=appointments)

@patient_bp.route('/medical_history')
@login_required
def medical_history():
    return render_template('patient/medical_history.html')


@patient_bp.route('/create_appointment', methods=['GET', 'POST'])
@login_required
def create_appointment():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    form = AppointmentForm()
    form.doctor.choices = [(d.id, d.full_name) for d in Doctor.query.all()]

    if form.validate_on_submit():
        new_appointment = Appointment(
            patient_id=patient.id,
            doctor_id=form.doctor.data,
            date_time=form.date_time.data,
            reason=form.reason.data,
            status='pending'
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Randevu oluşturuldu! Onay bekleniyor.')
        return redirect(url_for('patient.dashboard'))

    return render_template('patient/create_appointment.html', form=form)

from models import Symptom
from forms import SymptomForm

@patient_bp.route('/symptom_form', methods=['GET', 'POST'])
@login_required
def symptom_form():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    form = SymptomForm()

    if form.validate_on_submit():
        symptom = Symptom(
            patient_id=patient.id,
            fever=form.fever.data,
            fever_temperature=form.fever_temperature.data if form.fever.data else None,
            description=form.description.data,
            created_at=datetime.utcnow()
        )
        db.session.add(symptom)
        db.session.commit()
        flash('Semptom bilgisi kaydedildi!')
        return redirect(url_for('patient.dashboard'))

    return render_template('patient/symptom_form.html', form=form)



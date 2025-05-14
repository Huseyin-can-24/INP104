from models import db, User, Patient, Appointment, Doctor, Symptom
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import redirect, url_for, flash
from forms import AppointmentForm, SymptomForm
from datetime import datetime, time, date

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
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    symptoms = Symptom.query.filter_by(patient_id=patient.id).order_by(Symptom.created_at.desc()).all()
    return render_template('patient/medical_history.html', symptoms=symptoms)

@patient_bp.route('/create_appointment', methods=['GET', 'POST'])
@login_required
def create_appointment():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    form = AppointmentForm()
    
    # Doktor seçeneklerini güncelle
    doctors = Doctor.query.join(User).all()
    form.doctor.choices = [(d.id, f"Dr. {d.user.first_name} {d.user.last_name}") for d in doctors]

    if form.validate_on_submit():
        # Tarih ve saati birleştir
        appointment_datetime = datetime.combine(form.date.data, form.time.data)
        
        new_appointment = Appointment(
            patient_id=patient.id,
            doctor_id=form.doctor.data,
            date_time=appointment_datetime,
            reason=form.reason.data,
            status='pending'
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Randevu oluşturuldu! Doktor onayı bekleniyor.', 'info')
        return redirect(url_for('patient.dashboard'))

    return render_template('patient/create_appointment.html', form=form)

@patient_bp.route('/view_prescription/<int:appointment_id>')
@login_required
def view_prescription(appointment_id):
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    # Appointment ve ilişkili verileri tek sorguda çekelim
    appointment = Appointment.query.join(Doctor).join(User, Doctor.user_id == User.id)\
        .filter(Appointment.id == appointment_id)\
        .first_or_404()
    
    if appointment.patient_id != patient.id:
        flash('Bu reçeteyi görüntüleme yetkiniz yok!', 'error')
        return redirect(url_for('patient.dashboard'))
    
    return render_template('patient/view_prescription.html', appointment=appointment)

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
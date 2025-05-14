from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Doctor, Appointment, db, Prescription
from forms import PrescriptionForm

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/dashboard')
@login_required
def dashboard():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    pending_appointments = Appointment.query.filter_by(doctor_id=doctor.id, status='pending').all()
    confirmed_appointments = Appointment.query.filter_by(doctor_id=doctor.id, status='confirmed').all()
    return render_template('doctor/dashboard.html',
                           pending_appointments=pending_appointments,
                           confirmed_appointments=confirmed_appointments)

@doctor_bp.route('/appointment/<int:appointment_id>/<action>', methods=['POST'])
@login_required
def handle_appointment(appointment_id, action):
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.doctor_id != doctor.id:
        flash('Bu işlem için yetkiniz yok!', 'error')
        return redirect(url_for('doctor.dashboard'))
    
    if action == 'accept':
        appointment.status = 'confirmed'
        flash('Randevu onaylandı!', 'success')
    elif action == 'reject':
        appointment.status = 'rejected'
        flash('Randevu reddedildi!', 'info')
    
    db.session.commit()
    return redirect(url_for('doctor.dashboard'))

@doctor_bp.route('/write_prescription/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def write_prescription(appointment_id):
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.doctor_id != doctor.id:
        flash('Bu işlem için yetkiniz yok!', 'error')
        return redirect(url_for('doctor.dashboard'))
    
    form = PrescriptionForm()
    
    if form.validate_on_submit():
        prescription = Prescription(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            doctor_id=doctor.id,
            medications=form.medications.data,
            instructions=form.instructions.data
        )
        db.session.add(prescription)
        db.session.commit()
        flash('Reçete başarıyla yazıldı!', 'success')
        return redirect(url_for('doctor.dashboard'))
    
    return render_template('doctor/write_prescription.html', form=form, appointment=appointment)
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Doctor, Appointment

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


@doctor_bp.route('/patients')
@login_required
def patients():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()

    # Bu doktorla en az bir randevusu olan hastaları listele
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patient_ids = list({app.patient_id for app in appointments})
    patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()

    return render_template('doctor/patient_list.html', patients=patients)

@doctor_bp.route('/patient/<int:patient_id>')
@login_required
def patient_detail(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    symptoms = Symptom.query.filter_by(patient_id=patient_id).order_by(Symptom.created_at.desc()).all()
    return render_template('doctor/patient_detail.html', patient=patient, symptoms=symptoms)

from models import db
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)  # modeller import edildikten sonra

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Modeller ve blueprint'ler
from models import User, Patient, Doctor, Appointment, Prescription, Symptom
from routes.auth import auth_bp
from routes.patient import patient_bp
from routes.doctor import doctor_bp

app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp, url_prefix='/patient')
app.register_blueprint(doctor_bp, url_prefix='/doctor')


@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'patient':
            return redirect(url_for('patient.dashboard'))
        elif current_user.role == 'doctor':
            return redirect(url_for('doctor.dashboard'))
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

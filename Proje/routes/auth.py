from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from models import db
from models import User, Patient, Doctor
from forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Kullanıcı bulunamadı')
            return render_template('auth/login.html', form=form)
        elif not user.check_password(form.password.data):
            flash('Yanlış şifre girdiniz')
            return render_template('auth/login.html', form=form)
        else:
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('patient.dashboard') if user.role == 'patient' else url_for('doctor.dashboard')
            return redirect(next_page)
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        if user.role == 'patient':
            db.session.add(Patient(user_id=user.id))
        else:
            db.session.add(Doctor(user_id=user.id))

        db.session.commit()
        flash('Tebrikler, kayıt oldunuz!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

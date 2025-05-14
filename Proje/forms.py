from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms import DateTimeField
from datetime import datetime
from wtforms import BooleanField, FloatField, SelectField, TextAreaField, SubmitField, DateField, TimeField

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    first_name = StringField('Ad', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Soyad', validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Hesap Türü', choices=[('patient', 'Hasta'), ('doctor', 'Doktor')])
    submit = SubmitField('Kayıt Ol')


class AppointmentForm(FlaskForm):
    doctor = SelectField('Doktor Seçiniz', coerce=int, validators=[DataRequired()])
    date = DateField('Tarih', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Saat', format='%H:%M', validators=[DataRequired()])
    reason = TextAreaField('Randevu Nedeni', validators=[DataRequired()])
    submit = SubmitField('Randevu Oluştur')

class SymptomForm(FlaskForm):
    fever = BooleanField('Ateş Var mı?')
    fever_temperature = FloatField('Ateş Sıcaklığı (°C)')
    description = TextAreaField('Semptom Açıklaması', validators=[DataRequired()])
    submit = SubmitField('Kaydet')


class PrescriptionForm(FlaskForm):
    medications = TextAreaField('İlaçlar', validators=[DataRequired()])
    instructions = TextAreaField('Kullanım Talimatları', validators=[DataRequired()])
    submit = SubmitField('Reçeteyi Kaydet')
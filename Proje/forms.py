from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo
from wtforms import DateTimeField, TextAreaField
from wtforms import BooleanField, FloatField

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Parola', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Parola', validators=[DataRequired()])
    confirm_password = PasswordField('Parola Tekrar', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('patient', 'Hasta'), ('doctor', 'Doktor')], validators=[DataRequired()])
    submit = SubmitField('Kayıt Ol')


class AppointmentForm(FlaskForm):
    doctor = SelectField('Doktor', coerce=int, validators=[DataRequired()])
    date_time = DateTimeField('Randevu Tarihi/Saati (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    reason = TextAreaField('Randevu Nedeni', validators=[DataRequired()])
    submit = SubmitField('Randevu Oluştur')

class SymptomForm(FlaskForm):
    fever = BooleanField('Ateş Var mı?')
    fever_temperature = FloatField('Ateş Sıcaklığı (°C)')
    description = TextAreaField('Semptom Açıklaması', validators=[DataRequired()])
    submit = SubmitField('Kaydet')

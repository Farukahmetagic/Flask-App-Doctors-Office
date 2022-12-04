from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError, Email

class CreateUserForm(FlaskForm):
    username = StringField(label='Username: ', validators=[Length(min=5, max=30), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Enter Password: ', validators=[Length(min=4, max=50), DataRequired()])
    password2 = PasswordField(label='Repeat password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    email = StringField(label='E-mail', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Log In')


class TerminReservationForm(FlaskForm):
    termin = StringField(label='Unesite vrijeme termina u formatu: "hh:mm"', validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField(label='Rezervisite termin')


class TerminDeleteForm(FlaskForm):
    submit = SubmitField(label='Otkazi Termin')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    location = StringField('Location (Adress)',validators=[DataRequired(), Length(min=2, max=50)])
    size = FloatField('Size (approximate)') #validators=[DataRequired(), NumberRange(0,100)])
    depth = FloatField('Depth (Approximate)')#, validators=[DataRequired()])
    photo = PasswordField('Photo', validators=[DataRequired()])
    #confirm_password = PasswordField('Confirm Password',
    #                                 validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DriverForm(FlaskForm):
    pothole_number = IntegerField('WO-ID', default=100)
    submitroute = SubmitField('Get Route')
    submitcompleted = SubmitField('Completed route')


class PotholeCompletedForm(FlaskForm):
    pothole_number = StringField('WO-ID', validators=[DataRequired()])
    submit = SubmitField('Completed Pothole')



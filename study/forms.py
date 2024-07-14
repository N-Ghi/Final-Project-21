from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    school = StringField('School/College Name', validators=[DataRequired(), Length(max=100)])
    primary_language = SelectField('Primary Language', choices=[('english', 'English'), ('french', 'French')], validators=[DataRequired()])
    secondary_languages = SelectMultipleField('Secondary Languages', choices=[('english', 'English'), ('french', 'French')], coerce=str)
    days = SelectMultipleField(u'Select your days availability', choices=[('m', 'Monday'), ('t', 'Tuesday'), ('w', 'Wednesday'), ('th', 'Thursday'), ('f', 'Friday'), ('s', 'Saturday'), ('su', 'Sunday')], validators=[InputRequired()])
    times = SelectMultipleField(u'Select your time availability', choices=[('m', 'Morning'), ('a', 'Afternoon'), ('e', 'Evening')], validators=[InputRequired()])
    strong_subjects = SelectMultipleField(u'Select your strong subjects', choices=[('c++', 'C++'), ('py', 'Python'), ('js', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS')], validators=[InputRequired()])
    weak_subjects = SelectMultipleField(u'Select your weak subjects', choices=[('c++', 'C++'), ('py', 'Python'), ('js', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS')], validators=[InputRequired()])
    submit = SubmitField('Complete Profile')

class VerifyEmailForm(FlaskForm):
    otp = StringField('Verify your email', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify')
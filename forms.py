"""Forms for adopt app."""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, URL, Optional, AnyOf, Length
from email_validator import validate_email

class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username:", validators=[InputRequired(), Length(0, 20)])
    password = PasswordField("Password:", validators=[InputRequired(), Length(0,30)])
    email = StringField("Email:", validators=[InputRequired(), Length(0, 50), Email()])
    first_name = StringField("First:", validators=[InputRequired(), Length(0, 30)])
    last_name = StringField("Last:", validators=[InputRequired(), Length(0, 30)])
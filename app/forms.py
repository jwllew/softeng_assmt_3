from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, Regexp

# from website.models import User, Project
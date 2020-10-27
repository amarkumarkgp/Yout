from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import validators


class ContactForm(FlaskForm):
    name = StringField(u'Full Name', [validators.DataRequired(), validators.length(max=50)])
    email = StringField('Email', [validators.DataRequired(), validators.length(max=100),
                                  validators.Email(message='Please enter a valid email address.')])
    message = TextAreaField(u'Message', [validators.optional(), validators.length(max=500, min=20)])


class SignUpForm(FlaskForm):
    name = StringField(u'Name', [validators.DataRequired(message='Please enter the name'), validators.length(max=6)])
    email = StringField(u'Email', [validators.DataRequired(), validators.length(max=100),
                                   validators.Email(message='Not a valid email address.')])
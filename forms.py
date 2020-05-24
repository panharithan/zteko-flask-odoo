from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime
default_finger_print_ip = '192.168.1.201'
default_odoo_ip = '192.168.1.170'
default_odoo_db_name = 'VTG-DB'
default_odoo_email = 'zteko'
default_odoo_password = '123'


class QueryForm(FlaskForm):
    finger_print_ip = StringField('IP address of Finger Print',
                                  default=default_finger_print_ip,
                           validators=[DataRequired(), Length(min=2, max=20)])
    odoo_ip = StringField('IP Address of Odoo', default=default_odoo_ip,
                        validators=[DataRequired()])
    odoo_db_name = StringField('Database Name of Odoo', default=default_odoo_db_name,
                          validators=[DataRequired()])
    odoo_email = StringField('Email of Odoo user', default=default_odoo_email,
                          validators=[DataRequired()])
    odoo_password = PasswordField("Password of Odoo user")
    entry_date = DateField('Entry Date (Year / Month / Day)', default=datetime.today())
    submit = SubmitField('Report')

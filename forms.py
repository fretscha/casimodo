# -*- coding: utf-8 -*-
from flask.wtf import Form, TextField, PasswordField, validators


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging

from flask import Flask, session, render_template
from flask import redirect, url_for, request, make_response

from flask.ext.sqlalchemy import SQLAlchemy

from flask_kvsession import KVSessionExtension
from simplekv.db.sql import SQLAlchemyStore

from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm


app = Flask(__name__)
app.secret_key = os.urandom(128)
app.config.from_object('settings.DevelopmentConfig')
toolbar = DebugToolbarExtension(app)


# SQLAlchemy
db = SQLAlchemy(app)





# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))





@app.before_first_request
def create_user():
    pass

# KVSession
store = SQLAlchemyStore(db.engine, db.metadata, 'sessions')
kvsession = KVSessionExtension(store, app)


@app.route('/debug', methods=['GET'])
def debug():

    response = make_response(repr(session))
    response.content_type = 'text/plain'
    return response


@app.route('/cas/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(session['service'])
    if request.method == 'GET':
        service = request.args.get('service', app.config['DEFAULT_SERVICE_URL'])
        session['service'] = service
        return render_template('login.html', form=form)


@app.route('/cas/logout',  methods=['GET'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    shandler = logging.StreamHandler(sys.stdout)
    shandler.setLevel(logging.DEBUG)
    app.logger.addHandler(shandler)
    app.run()

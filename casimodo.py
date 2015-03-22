#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import redis
from datetime import timedelta
import logging


from flask import Flask, session, render_template
from flask import redirect, url_for, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm

DEFAULT_SERVICE_URL = '/debug'


app = Flask(__name__)
app.debug = True


app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# set the secret key. keep this really secret:
app.secret_key = bytearray(os.urandom(64))
toolbar = DebugToolbarExtension(app)

app.redis = redis.StrictRedis('localhost', port=6379, db=0)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=300)


@app.route('/debug', methods=['GET'])
def debug():
    return "you are logged in"


@app.route('/cas/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(session['service'])
    if request.method == 'GET':
        service = request.args.get('service', DEFAULT_SERVICE_URL)
        session['service'] = service
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    shandler = logging.StreamHandler(sys.stdout)
    shandler.setLevel(logging.DEBUG)
    app.logger.addHandler(shandler)
    app.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging
from datetime import timedelta
import pickle

import redis


from flask import Flask, session, render_template, flash
from flask import redirect, url_for, request
from flask_wtf.csrf import CsrfProtect


from flask_kvsession import KVSessionExtension, SessionID
from simplekv.memory.redisstore import RedisStore

from flask_debugtoolbar import DebugToolbarExtension

from forms import LoginForm


app = Flask(__name__)

store = RedisStore(redis.StrictRedis())

KVSessionExtension(store, app)
csrf = CsrfProtect(app)

app.secret_key = os.urandom(128)
app.config.from_object('settings.DevelopmentConfig')
toolbar = DebugToolbarExtension(app)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(
        seconds=app.config['SESSION_TIMEOUT'])


@app.route('/debug', methods=['GET'])
def debug():
    keys = store.keys()
    value = dict()
    ttl = dict()
    for k in keys:
        value[k] = pickle.loads(store.redis.get(k))
        ttl[k] = store.redis.ttl(k)
    return render_template('debug.html', keys=keys, value=value, ttl=ttl)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        session['username'] = request.form['username']
        flash('You were logged in')
        return redirect(session['service'])
    if request.method == 'GET':
        service = request.args.get(
            'service', app.config['DEFAULT_SERVICE_URL'])
        session['service'] = service
        return render_template('login.html', form=form)


@app.route('/logout',  methods=['GET'])
def logout():
    # remove the username from the session if it's there
    session.destroy()
    return redirect(url_for('debug'))


@csrf.error_handler
def csrf_error(reason):
    return render_template('error.html', reason=reason)


if __name__ == '__main__':
    shandler = logging.StreamHandler(sys.stdout)
    shandler.setLevel(logging.DEBUG)
    app.logger.addHandler(shandler)
    app.run()

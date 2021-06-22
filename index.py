#!/usr/bin/python
import time
import hashlib
import json
import logging
import hashlib

import requests
from flask import Flask, render_template, url_for
from flask import Response, stream_with_context

from soco import SoCo

werkzeug = logging.getLogger('werkzeug')
werkzeug.setLevel(logging.WARNING)

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

app = Flask(__name__)

app.config.from_pyfile('settings.py')

sonos = SoCo(app.config['SPEAKER_IP'])
coordinator = sonos
#coordinator = sonos.group.coordinator

@app.route("/play")
def play():
    coordinator.play()
    return 'Ok'


@app.route("/pause")
def pause():
    coordinator.pause()
    return 'Ok'


@app.route("/next")
def next():
    coordinator.next()
    return 'Ok'


@app.route("/previous")
def previous():
    coordinator.previous()
    return 'Ok'


@app.route("/info-light")
def info_light():
    track = coordinator.get_current_track_info()
    return json.dumps(track)

@app.route("/version")
def version():
    filehash_html = hashlib.md5()
    filehash_html.update(open('templates/index.html').read())
    filehash_css = hashlib.md5()
    filehash_css.update(open('static/css/main.css').read())
    version = filehash_html.hexdigest()+filehash_css.hexdigest()
    return json.dumps(version)

@app.route("/info")
def info():
    track = coordinator.get_current_track_info()
    #track['image'] = get_track_image(track['artist'], track['album'])
    track['image'] = track['album_art']
    if track['image'] == "":
	track['image'] = url_for('static', filename='img/blank2.jpg')
    log.info(track)
    return json.dumps(track)


@app.route("/")
def index():
    track = coordinator.get_current_track_info()
    #track['image'] = get_track_image(track['artist'], track['album'])
    track['image'] = track['album_art']
    if track['image'] == "":
	track['image'] = url_for('static', filename='img/blank2.jpg')
    return render_template('index.html', track=track)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

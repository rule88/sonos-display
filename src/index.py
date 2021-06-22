import json
import logging
import hashlib
import soco

from flask import Flask, render_template, url_for
from settings import settings

werkzeug = logging.getLogger('werkzeug')
werkzeug.setLevel(logging.WARNING)

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

app = Flask(__name__)

display_sonos = soco.discovery.by_name(settings.speaker_name)


@app.route("/play")
def play():
    display_sonos.play()
    return 'Ok'


@app.route("/pause")
def pause():
    display_sonos.pause()
    return 'Ok'


@app.route("/next")
def next():
    display_sonos.next()
    return 'Ok'


@app.route("/previous")
def previous():
    display_sonos.previous()
    return 'Ok'


@app.route("/info-light")
def info_light():
    track = display_sonos.get_current_track_info()
    return json.dumps(track)


@app.route("/version")
def version():
    filehash_html = hashlib.md5()
    filehash_html.update(open('templates/index.html').read())
    filehash_css = hashlib.md5()
    filehash_css.update(open('static/css/main.css').read())
    version = filehash_html.hexdigest() + filehash_css.hexdigest()
    return json.dumps(version)


@app.route("/info")
def info():
    track = display_sonos.get_current_track_info()
    # track['image'] = get_track_image(track['artist'], track['album'])
    track['image'] = track['album_art']
    if track['image'] == "":
        track['image'] = url_for('static', filename='img/blank2.jpg')
    log.info(track)
    return json.dumps(track)


@app.route("/")
def index():
    track = display_sonos.get_current_track_info()
    # track['image'] = get_track_image(track['artist'], track['album'])
    track['image'] = track['album_art']
    if track['image'] == "":
        track['image'] = url_for('static', filename='img/blank2.jpg')
    return render_template('index.html', track=track)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

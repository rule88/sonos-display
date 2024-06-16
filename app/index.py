import json
import logging
import hashlib
import time

import soco
import cachetools.func

from flask import Flask, render_template, url_for
from settings import settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('sonos-display')
logger.setLevel(logging.INFO)

app = Flask('sonos-display')


@cachetools.func.ttl_cache(ttl=60)
def get_sonos():
    for speaker in soco.discovery.scan_network():
        if speaker.get_speaker_info()['zone_name'] == settings.speaker_name:
            return speaker
    raise soco.SoCoException(f'couldn\'t find sonos by provided name "{settings.speaker_name}"')


@app.route("/play")
def play():
    get_sonos().play()
    return 'Ok'


@app.route("/pause")
def pause():
    get_sonos().pause()
    return 'Ok'


@app.route("/next")
def next():
    get_sonos().next()
    return 'Ok'


@app.route("/previous")
def previous():
    get_sonos().previous()
    return 'Ok'


@app.route("/info-light")
def info_light():
    track = get_sonos().get_current_track_info()
    return json.dumps(track)


@app.route("/version")
def version():
    filehash_html = hashlib.md5()
    filehash_html.update(open('templates/index.html', "r", encoding='utf-8').read().encode('utf-8'))
    filehash_css = hashlib.md5()
    filehash_css.update(open('static/css/main.css', "r", encoding='utf-8').read().encode('utf-8'))
    version = filehash_html.hexdigest() + filehash_css.hexdigest()
    return json.dumps(version)


@app.route("/info")
def info():
    track = get_sonos().get_current_track_info()
    # track['image'] = get_track_image(track['artist'], track['album'])
    track['image'] = track['album_art']
    if track['image'] == "":
        track['image'] = url_for('static', filename='img/blank2.jpg')
    logger.info(track)
    return json.dumps(track)


@app.route("/")
def index():
    track = get_sonos().get_current_track_info()
    # track['image'] = get_track_image(track['artist'], track['album'])
    track['image'] = track['album_art']
    if track['image'] == "":
        track['image'] = url_for('static', filename='img/blank2.jpg')
    return render_template('index.html', track=track)


try:
    logger.info(f'sonos used for peering: {get_sonos().get_speaker_info()}')
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=settings.port)
except soco.SoCoException as e:
    logger.info(f"{e}")
    time.sleep(10)
    exit(1)

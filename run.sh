# !/bin/bash

source .env

docker run --restart unless-stopped -d -e PORT=$PORT -e SPEAKER_NAME="$SPEAKER_NAME" --network host --name sonos-display rule88/sonos-display:latest

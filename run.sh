# !/bin/bash

source .env

docker build -t sonos-display:latest .
docker run --restart unless-stopped -d -e PORT=$PORT -e SPEAKER_NAME=$SPEAKER_NAME --network host --name sonos-display sonos-display:latest
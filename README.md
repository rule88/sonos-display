# Sonos Display

This project aims to provide an easy way to access the Album Art of a sonos system by serving a simple webpage.

## Usage

Before running anything, you should copy `.env.example` to `.env` and fill in or change it's variables.

When using docker-compose:
```bash
docker-compose up -d
```

When using docker directly (script will build image & run container)
```bash
./run.sh
```

The container requires to bind on the host network because of the auto-discovery. This way it will be able to find the 
sonos device even if it's IP has been changed.

Now that the container is running you should be able to navigate to `<host_ip>:<port>`, the album art of the currently
playing song should show up together with a banner providing some information about the song.
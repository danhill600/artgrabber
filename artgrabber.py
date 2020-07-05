#!/usr/bin/env python3

import subprocess
import agfunctions as af
import pylast
import mpd



network = pylast.LastFMNetwork(af.get_key())
client = af.connect_client()

album, artist, bio = af.new_album_operations(network, client)

while True:
    for line in client.idle():
        if af.check_for_new_album(album, client):
            album, artist, bio = af.new_album_operations(network, client)

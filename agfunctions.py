import pylast
import mpd
import os
import subprocess
import filecmp
#import urllib.request
import requests
import shutil
import time
import getpass
import random
from textwrap import TextWrapper

def get_key():
    try:
        with open('../apikey.secret', 'r') as apikey:
            API_KEY, API_SECRET = apikey.read().splitlines()[:2]
            return API_KEY
    except Exception as e:
            print(e)
            exit()

def connect_client():
    """Connect to MPD Client"""
    client = mpd.MPDClient()
    client.connect("localhost", 6600)
    return client

def new_album_operations(network, client):
    wrapper = TextWrapper(break_long_words=True)
    artist, album = get_artist_and_album(network, client)

    print(album)
    print("---------------")
    bio = wrapper.wrap(get_bio(artist))
    linecounter=0
    with open("bio2.txt", "w") as bio_txt2:
        for line in bio:
            if linecounter < 20:
                linecounter +=1
                bio_txt2.write(line)
                print(line)
            elif linecounter == 20:
                linecounter += 1
                bio_txt2.write(line + "...")
                print(line + "...")
    print("---------------")
    get_local_art(network, client)
    print("---------------")
    return album, artist, bio

def get_artist_and_album(network, client):
    """print the artist and album"""

    try:
       artist = client.currentsong()['artist']
       album = client.currentsong()['album']

       artist = pylast.Artist(artist, network)
       album = network.get_album(artist, album)
    except:
        artist = 'Primate'
        album = 'Greatest Hits'

    return artist, album

def get_bio(artist):
    """Print artist biography"""
    try:
        bio = artist.get_bio_content(language="en")
    except:
        bio = "No bio found."
    if bio is None:
        bio = "No Bio Found."
    with open("bio.txt", "w") as bio_txt:
        for line in bio:
            bio_txt.write(line)
    return bio

def get_local_art(network, client):
    theimages = []
    musicdir= "/endo/music/"
    songfile=client.currentsong()['file']
    songdir = os.path.dirname(os.path.join(musicdir,songfile))
    for fname in os.listdir(songdir):
        if fname.endswith(('.png','.jpg','.jpeg','gif')):
            theimages.append(songdir + "/" + fname)
    if theimages:
        biggestimage = max(theimages, key=os.path.getsize)
        subprocess.call(['convert', '-resize', '400x400', biggestimage, 'cover.png'])
        print("local image written to artgrabber/cover.png")
    else:
        get_lastfm_art(network, client)

def get_lastfm_art(network, client):
    album = network.get_album(client.currentsong()['artist'],
                              client.currentsong()['album'])
    try:

        url = album.get_cover_image().encode("utf-8")
        response = requests.get(url, stream =True)

        if response.status_code == 200:
            with open('cover.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            subprocess.call(['convert', '-resize', '400x400', 'cover.png', 'cover.png'])
            del response
        print("Last.fm image written to cover.png")
    except:
        print("couldn't find a cover at last.fm, either.")
        enjoy_monkey()

def check_for_new_album(album, client):
    """See if a new album is playing and if so reset the variable"""
    try:
        newalbum = client.currentSong['album']
    except:
        newalbum = 'Not Sure'
    if newalbum == album:
        print( "no new album.")
        return False
    else:
        print( "new album.")
        return True

def enjoy_monkey():
    print("Enjoy monkey.")
    monkeydir = "/endo/pics/monkeys"
    monkey= monkeydir + "/" +random.choice(os.listdir(monkeydir))
    subprocess.call(['convert', '-resize', '400x400', monkey, 'cover.png'])

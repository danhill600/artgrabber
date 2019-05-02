import pylast
import mpd
import os
import filecmp
import urllib.request
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
            print_exc()
            sys.exit()

def connect_client():
    """Connect to MPD Client"""
    client = mpd.MPDClient()
    client.connect("localhost", 6600)
    currentSong = client.currentsong()
    return currentSong

def new_album_operations(network):
    currentSong=connect_client()
    wrapper = TextWrapper(break_long_words=True)
    print("---------------")
    album, artist =get_artist_and_album(network, currentSong)
    print(album)
    print("---------------")
    bio = wrapper.wrap(get_bio(network, currentSong))
    for line in bio:
        print(line)
    print("---------------")
    write_cover(network, currentSong, album)
    return currentSong, album, artist, bio

def get_artist_and_album(network, currentSong):
    """print the artist and album"""
    artist = network.get_artist(currentSong['artist'])
    album = network.get_album(currentSong['artist'],currentSong['album'])
    return album, artist

def get_bio(network, currentSong):
    """Print artist biography"""
    artist = network.get_artist(currentSong['artist'])
    try:
        bio = artist.get_bio_content(language="en")
    except AttributeError:
        bio = "No bio found."
    except pylast.MalformedResponseError:
        bio= "I messed up reading the bio some kinda way."
    except pylast.WSError:
        bio= "I don't know, last fm is messing up the bio somehow, sorry."
    with open("bio.txt", "w") as bio_txt:
        for line in bio:
            bio_txt.write(line)
    return bio

def write_cover(network, currentSong, album): #do I even need network here?
    if get_local_art(currentSong):
        pass
    else:
       get_lastfm_art(album)

def get_local_art(currentSong):
    theimages = []
    musicdir= "/home/" + getpass.getuser() + "/endo/music/"
    songdir = os.path.dirname(os.path.join(musicdir,currentSong['file']))
    for fname in os.listdir(songdir):
        if fname.endswith(('.png','.jpg','.jpeg')):
            theimages.append(songdir + "/" + fname)
    if theimages:
        biggestimage = max(theimages, key=os.path.getsize)
        shutil.copy(biggestimage,'cover.png')
        print("local image written to artgrabber/cover.png")
        return True
    else:
        return False

def get_lastfm_art(album):
    print("no local image, trying last.fm...")
    try:
        img_url = album.get_cover_image()
        with urllib.request.urlopen(img_url) as response, open("cover.png", 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print(img_url + " written to artgrabber/cover.png")
    except pylast.WSError:
        print("Album info not found")
        enjoy_monkey()
    except AttributeError:
        print("couldn't find a cover.")
        enjoy_monkey()
    except TypeError:
        print("couldn't find a cover.")
        enjoy_monkey()

def check_for_new_album(album, network):
    """See if a new album is playing and if so reset the variable"""
    currentSong=connect_client()
    newalbum=network.get_album(currentSong['artist'],currentSong['album'])
    print("previous album was " + str(album))
    print("current album is " + str(newalbum))
    print(album==newalbum)
    if newalbum == album:
        return False
    else:
        return True

def enjoy_monkey():
    print("Enjoy monkey.")
    monkeydir = "/home/" + getpass.getuser() + "/endo/pics/monkeys"
    monkey= monkeydir + "/" +random.choice(os.listdir(monkeydir))
    shutil.copy(monkey,'cover.png')

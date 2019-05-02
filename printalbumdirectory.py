import mpd
import pylast
import os
import shutil
import getpass


try:
    with open('../apikey.secret', 'r') as apikey:
        API_KEY, API_SECRET = apikey.read().splitlines()[:2]
except Exception as e:
        print_exc()
        sys.exit()

##Connect to MPD client
client = mpd.MPDClient()
client.connect("localhost", 6600)
currentSong = client.currentsong()

#print(currentSong)
musicdir= "/home/" + getpass.getuser() + "/endo/music/"
songdir = os.path.dirname(os.path.join(musicdir,currentSong['file']))
#print(songdir)

#print(os.listdir(songdir))

theimages = []
for fname in os.listdir(songdir):
    if fname.endswith(('.png','.jpg','.jpeg')):
        theimages.append(songdir + "/" + fname)
if theimages:
    biggestimage = max(theimages, key=os.path.getsize)
    shutil.copy(biggestimage,'cover.png')
    print("local art written to cover.png")
else:
    print("local art not found.")

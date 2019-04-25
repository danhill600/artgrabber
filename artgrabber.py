import pylast
import mpd

try:
    with open('../apikey.secret', 'r') as apikey:
        API_KEY, API_SECRET = apikey.read().splitlines()[:2]
    with open('../login.secret', 'r') as login:
        USERNAME, PASSWORD_HASH = login.read().splitlines()[:2]
except Exception as e:
        print_exc()
        sys.exit()

##Connect to MPD client
client = mpd.MPDClient()
client.connect("localhost", 6600)
currentSong = client.currentsong()

print(currentSong)



network = pylast.LastFMNetwork(api_key=API_KEY)

#get mpd song artist
#for now pretending it's Deerhunter
artist = network.get_artist(client.current())

#bio = artist.get_bio_content(language="en")
#print(bio)
#get artist inf


#print artist info

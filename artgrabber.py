import os
import agfunctions as af
import pylast


network = pylast.LastFMNetwork(af.get_key())
currentSong, album, artist, bio=af.new_album_operations(network)

print("I'm going to start listening to mpd, and I'll spit out some info\n")
print("and change cover.png when a new album starts playing.  Just do a janky\n")
print("^C to quit\n")


# okay for now this all assumes an 'mpc idleloop > testfifo' has already
#been started, but you should get the script to make and start the fifo

while True:
    with open("testfifo", "r") as fin:
        for line in fin:
            print("The fifo has received a player event.\n")
            if af.check_for_new_album(album, network):
                print("new album detected!")
                currentSong, album, artist, bio=af.new_album_operations(network)
            else:
                pass


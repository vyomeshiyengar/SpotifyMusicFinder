# export SPOTIPY_CLIENT_ID='07279f7ca3094ddb999e7e2fec4bcc4d'
# export SPOTIPY_CLIENT_SECRET='CLIENTSECRET'
# export SPOTIPY_REDIRECT_URI='https://www.google.ca/'

import os
import sys
import json
import spotipy
import webbrowser
import spotipy as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import numpy as np

# setup
    #jbjiwxnlxxr53e7awx4vu4y83
global username
username = sys.argv[0]
scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private'

    #erase cashe prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cashe-{username}")
    token = util.prompt_for_user_token(username, scope)

    #create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

devices = spotifyObject.devices()
deviceID = devices['devices'][0]['id']

# entry page, currently playing

# search artist and display most recent single name, album cover, genre, followers

def options(): 
    print ("1. Listen to artist's top hits")
    print ("2. Find similar artists")
    print ("3. Play the artist's most recent album")
    print("4. Exit")
    global response
    response = input("What would you like to do: ")

def artistInfo():
    artistNewResults = spotifyObject.search(artistNew, 1, 0, 'artist')
    name = artistNewResults["artists"]["items"][0]["name"]
    genre = artistNewResults["artists"]["items"][0]["genres"][0]
    ranking = artistNewResults["artists"]["items"][0]["popularity"]
    followers = artistNewResults["artists"]["items"][0]["followers"]["total"]
    artistID = artistNewResults["artists"]["items"][0]["id"]
    artistAlbums = spotifyObject.artist_albums(artistID)
    recentAlbum = artistAlbums["items"][0]["name"]
    recentAlbumDate = artistAlbums["items"][0]["release_date"]
    recentAlbumURI = artistAlbums["items"][0]["id"]
    recentAlbumImageDetails = spotifyObject.album(recentAlbumURI)
    print()
    print(name + " features in " + genre + ", is currently ranked at " + str(ranking) + ", and has " + str(followers) + " followers. Their most recent album was titled " + recentAlbum + " released on " + recentAlbumDate + ". The following is the album cover.")
    print()
    webbrowser.open(recentAlbumImageDetails["images"][0]["url"])

def topHits():
    u = 0
    while u <= 15:
        artistNewResults = spotifyObject.search(artistNew, 1, 0, 'artist')
        artistName = artistNewResults["artists"]["items"][0]["name"]
        artistID = artistNewResults["artists"]["items"][0]["id"]
        topTracks = spotifyObject.artist_top_tracks(artistID, 'CA')
        topTrackAlbumURI = topTracks["tracks"][u]["album"]["uri"]
        topTrackAlbumName = topTracks["tracks"][u]["album"]["name"]
        topTrackName = topTracks["tracks"][u]["name"]
        topTrackURI = topTracks["tracks"][u]["uri"]
        topTrackURIList=(topTrackURI)
        print()
        print(f"Playing {topTrackName}")
        print()
        spotifyObject.start_playback(deviceID, None, [topTrackURIList])
        print()
        print ("1. Add to playlist")
        print ("2. Play next top song")
        print("3. Exit")
        print("4. Play album")
        print()
        global responseHits
        responseHits = input("What would you like to do next?: ")

        if responseHits == "1":
            userPlaylists = spotifyObject.current_user_playlists()
            for name in userPlaylists["items"]:
                namePlaylist = name["name"]
                if namePlaylist == artistName + " Favourites":
                        playlistVar = (namePlaylist.index(artistName + " Favourites"))
                        playlistID = userPlaylists["items"][playlistVar]["id"]
                        playlistTracks = spotifyObject.playlist_tracks(playlistID)
                        for items in playlistTracks["items"]:
                            if items["track"]["uri"]==topTrackURIList:
                                print("Track already in playlist")
                                print()
                                print ("2. Play next top song")
                                print("3. Exit")
                                print("4. Listen to album")
                                print()
                                responseHits = input("What would you like to do next?: ")    
                                break    
                            
                            else:
                                spotifyObject.user_playlist_add_tracks(username, playlistID, [topTrackURIList])
                                print("Track has been added")
                                print()
                                print ("2. Play next song")
                                print("3. Exit")
                                print("4. Listen to album")
                                print()
                                responseHits = input("What would you like to do next?: ")
                                break
                else:
                    newPlaylist = spotifyObject.user_playlist_create("jbjiwxnlxxr53e7awx4vu4y83", artistName + " Favourites")
                    spotifyObject.user_playlist_add_tracks(username, newPlaylist["id"], [topTrackURIList])
                    print("Track has been added")
                    print()
                    print ("2. Play next song")
                    print("3. Exit")
                    print("4. Listen to album")
                    print()
                    responseHits = input("What would you like to do next?: ")
                    break
                break
        if responseHits == "2":
            u+=1
        if responseHits == "3":
            responseHits = "z"
            break
        if responseHits == "4":
            print()
            print(f"Playing {topTrackAlbumName}")
            spotifyObject.start_playback(deviceID,topTrackAlbumURI)
            print()
            print ("1. Add to playlist")
            print ("2. Play next song")
            print("3. Exit")
            print()
            responseAlbum = input("What would you like to do next?: ")
            while u <= 15:
                if responseAlbum == "1":
                    userPlaylists = spotifyObject.current_user_playlists()
                    for name in userPlaylists["items"]:
                        namePlaylist = name["name"]
                        if namePlaylist == artistName + " Favourites":
                            playlistVar = (namePlaylist.index(artistName + " Favourites"))
                            playlistID = userPlaylists["items"][playlistVar]["id"]
                            playlistTracks = spotifyObject.playlist_tracks(playlistID)
                            for items in playlistTracks["items"]:
                                if items["track"]["uri"]==topTrackURIList:
                                    print("Track already in playlist")
                                    print()
                                    print ("2. Play next song")
                                    print("3. Exit")
                                    print()
                                    responseAlbum = input("What would you like to do next?: ")
                                    break    
                                else:
                                    spotifyObject.user_playlist_add_tracks(username, playlistID, [topTrackURIList])
                                    print("Track has been added")
                                    print()
                                    print ("2. Play next song")
                                    print("3. Exit")
                                    print()
                                    responseAlbum = input("What would you like to do next?: ")
                                    break      
                        else:
                            newPlaylist = spotifyObject.user_playlist_create("jbjiwxnlxxr53e7awx4vu4y83", artistName + " Favourites")
                            spotifyObject.user_playlist_add_tracks(username, newPlaylist["id"], [topTrackURIList])
                            print("Track has been added")
                            print()
                            print ("2. Play next song")
                            print("3. Exit")
                            print()
                            responseAlbum = input("What would you like to do next?: ")
                            break
                        break
                if responseAlbum == "2":
                    spotifyObject.next_track(deviceID)
                    currentlyPlaying = spotifyObject.currently_playing()
                    trackName = currentlyPlaying["item"]["name"]
                    print()
                    print(f"Playing {trackName}")
                    print()
                    print ("1. Add to playlist")
                    print ("2. Play next song")
                    print("3. Exit")
                    print()
                    responseAlbum = input("What would you like to do next?: ")
                if responseAlbum == "3":
                    u=19
                    break
    
def similarArtistsSearch():
    global artistNew
    artistNew = input("Which artist would you like to listen to: ")
    global artistNewResults
    artistNewResults = spotifyObject.search(similarArtistsNameList[int(artistNew)], 1, 0, 'artist')
    global name
    name = artistNewResults["artists"]["items"][0]["name"]
    artistNew = name
    genre = artistNewResults["artists"]["items"][0]["genres"][0]
    ranking = artistNewResults["artists"]["items"][0]["popularity"]
    followers = artistNewResults["artists"]["items"][0]["followers"]["total"]
    artistID = artistNewResults["artists"]["items"][0]["id"]
    artistAlbums = spotifyObject.artist_albums(artistID)
    recentAlbum = artistAlbums["items"][0]["name"]
    recentAlbumDate = artistAlbums["items"][0]["release_date"]
    recentAlbumURI = artistAlbums["items"][0]["id"]
    recentAlbumImageDetails = spotifyObject.album(recentAlbumURI)
    print()
    print(f"{name} features in {genre}, is currently ranked at {str(ranking)} and has {str(followers)} followers. Their most recent album was titled {recentAlbum} released on {recentAlbumDate}. The following is the album cover.")
    print()
    webbrowser.open(recentAlbumImageDetails["images"][0]["url"])
    options()

def similarArtists():
    z=0
    global similarArtistsList
    global similarArtistsNameList
    similarArtistsList = []
    similarArtistsNameList = []
    artistNewResults = spotifyObject.search(artistNew, 1, 0, 'artist')
    artistID = artistNewResults["artists"]["items"][0]["id"]
    relatedArtists = spotifyObject.artist_related_artists(artistID)
    for person in relatedArtists["artists"]:
        personName = person["name"]
        print(str(z)+ ": " + personName)
        similarArtistsList.append(relatedArtists["artists"][z]["uri"])
        similarArtistsNameList.append(relatedArtists["artists"][z]["name"])
        print()
        z+=1
        while z == 10:
            break
    similarArtistsSearch()

def topAlbum():
    artistNewResults = spotifyObject.search(artistNew, 1, 0, 'artist')
    artistID = artistNewResults["artists"]["items"][0]["id"]
    artistAlbums = spotifyObject.artist_albums(artistID)
    recentAlbum = artistAlbums["items"][0]["uri"]
    recentAlbumName = artistAlbums["items"][0]["name"]
    spotifyObject.start_playback(deviceID, recentAlbum)
    print()
    print(f"Playing {recentAlbumName}")
    print()
  
print()
print("Welcome to Music Finder!")
currentSong = spotifyObject.currently_playing()
trackName = currentSong["item"]["name"]
artist = currentSong["item"]["artists"][0]["name"]
print()
print(f"Currently playing {trackName} by {artist}")
print()

artistNew = input("Who would you like to find: ")

while artistNew == "x":
    print("See you next time!")
    artistNew = "z"
    break
else: 
    artistInfo()
    options()
    while response != "x": 
        if response == "1":
            topHits()
            print("See you next time!")
            response = "z"
            break
        if response == "2":
            similarArtists()
        if response == "3":
            topAlbum()
            print("1. Listen to artist's top hits")
            print ("2. Find similar artists")
            print("4. Exit")
            response = input("What would you like to do next?: ")
        while response == "4":
            print("See you next time!")
            response = "z"
            break
  
  
    # top hits - DONE 

        # play top song - DONE
        
        
            # add to playlist option - DONE

                # create playlist and add song - DONE

                # play album option - DONE

                    # play song - DONE

                    # add to playlist? - DONE

                        # yes - DONE

                        # no, next song - DONE

                        # exit - DONE

                # next song option - DONE

                    # add to playlist? - DONE

                            # yes - DONE

                            # no, next song - DONE

                            # exit - DONE
                # exit - DONE

            # next song option - DONE

            # exit - DONE

    # similar artists - DONE

        # display artists and allow selection - DONE

            # redirect to options - DONE

    # play most recent album - DONE

        # redirect to options - DONE

    # exit - DONE
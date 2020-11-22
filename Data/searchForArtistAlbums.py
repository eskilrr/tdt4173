import spotipy
import os
import datetime
from spotipy.oauth2 import SpotifyClientCredentials
os.environ['SPOTIPY_CLIENT_ID'] = '0352b9dc8c1b44f69aeee6cae24f0f53'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'c4003dba4d564ccaaaa23c1044f34b92'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def getArtistAlbums(artist_id, aNumber):
    meta = sp.artist_albums(artist_id, limit=aNumber)['items']
    album_ids = [album['id'] for album in meta if albumReleasedAfter2000(album['id'])]
    album_names = [album['id'] for album in meta if albumReleasedAfter2000(album['id'])]
    print("Number of albums: ", len(album_names))
    return [album_ids, album_names]

def albumReleasedAfter2000(album_id):
    release_year = sp.album(album_id)['release_date'].split("-")[0]
    if int(release_year) > 2000:
        return True
    else:
        return False

def getArtistName(artist_id):
    meta = sp.artist(artist_id)['name']
    return meta

def getSongsInAlbum(album_id): #Not including songs released before 2000
    meta = []
    song_ids = []
    song_names = []
    y = datetime.datetime.now() + datetime.timedelta(0, 5)
    while datetime.datetime.now() < y:
        try:
            meta = sp.album_tracks(album_id)['items']
            break
        except spotipy.SpotifyException as e:
            print(e)
            break
        except Exception as e:
            continue

    #Do not include if song title has remix or live in it
    for song in meta:
        name = song['name']
        if "live" in name or "remix" in name or "Live" in name or "Remix" in name or "Mix" in name or "Edit" in name\
                or "Version" in name or "Instrumental" in name or "Acoustic" in name:
            #print("Excluded: ", name)
            continue
        song_ids.append(song['id'])
        song_names.append(name)
    return [song_ids, song_names]

def getCatalogueFromArtist(artist_id, aNumber):
    song_ids = []
    song_names = []
    artist_albums = getArtistAlbums(artist_id, aNumber)[0]
    for a in artist_albums:
        album_songs = getSongsInAlbum(a)
        album_song_ids = album_songs[0]
        album_song_names = album_songs[1]
        for i, s in enumerate(album_song_names):
            if s not in song_names:
                song_ids.append(album_song_ids[i])
                song_names.append(s)
    return [song_ids, song_names]

#getArtistName("66CXWjxzNUsdJxJ2JdwvnR")
#ariana_cat = getCatalogueFromArtist("66CXWjxzNUsdJxJ2JdwvnR")
#print(len(ariana_cat[0]))

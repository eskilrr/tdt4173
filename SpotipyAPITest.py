import spotipy
import os
import pandas as pd

from spotipy.oauth2 import SpotifyClientCredentials
os.environ['SPOTIPY_CLIENT_ID'] = '0352b9dc8c1b44f69aeee6cae24f0f53'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'c4003dba4d564ccaaaa23c1044f34b92'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

def getAllArtistsFollowersFromTrack(track_id):
    meta = sp.track(track_id)
    artists = [item['id'] for item in meta['artists']]
    followers = 0
    popularities = []
    for artist in artists:
        features = getArtistFeaturesFromArtist(artist)
        popularities.append(features[0])
        followers += features[1]
    return [popularities, followers]


def getArtistFeaturesFromArtist(artist_id):
    meta = sp.artist(artist_id)
    return [meta['popularity'], meta['followers']['total']]

def getTrackFeatures(track_id):
    meta = sp.track(track_id)
    features = sp.audio_features(track_id)

    # meta
    name = meta['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    artists_features = getAllArtistsFollowersFromTrack(track_id)
    artist_popularity = artists_features[0]
    artist_followers = artists_features[1]

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, artist_popularity, artist_followers, release_date, length, popularity,
             danceability, acousticness, danceability, energy, instrumentalness, liveness,
             loudness, speechiness, tempo, time_signature]
    return track

def getDataFromTracklist(tracklist):
    features = ["name", "artist_popularity", "artist_followers", "release_date", "length", "popularity",
             "danceability", "acousticness", "danceability", "energy", "instrumentalness", "liveness",
             "loudness", "speechiness", "tempo", "time_signature"]
    transposed_tracklist = list(map(list, zip(*tracklist)))
    feature_dict = dict(zip(features, transposed_tracklist))
    return pd.DataFrame.from_dict(feature_dict)

#Printing features in global top 50
track_ids = getTrackIDs('ingebosse', '37i9dQZEVXbMDoHDwVN2tF')
tracklist = [getTrackFeatures(track_id) for track_id in track_ids]
df = getDataFromTracklist(tracklist)


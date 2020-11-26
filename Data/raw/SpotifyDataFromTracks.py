import spotipy
import os
import Data.raw.SpotifyTracksFromArtist as sa

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

def getKey(track_id):
    features = []
    while True:
        try:
            features = sp.audio_features(track_id)
            break
        except Exception as e:
            continue
    return [features[0]['key']]

def getExtraFeaturesFromTrack(track_id):
    meta = sp.track(track_id)
    artists = [artist['id'] for artist in meta['artists']]
    duration_ms = meta['duration_ms']
    popularity = meta['popularity']
    release_date = meta['album']['release_date']
    followers = 0
    popularities = []
    for artist in artists:
        features = getArtistFeaturesFromArtist(artist)
        popularities.append(features[0])
        followers += features[1]
    return ["", duration_ms, popularity, release_date, 0, max(popularities), followers, len(artists), artists]

def getAllArtistsFollowersFromTrack(track_id):
    meta = sp.track(track_id)
    artists = [artist['id'] for artist in meta['artists']]
    followers = 0
    popularities = []
    for artist in artists:
        features = getArtistFeaturesFromArtist(artist)
        popularities.append(features[0])
        followers += features[1]
    return [max(popularities), followers, len(artists), artists]


def getArtistFeaturesFromArtist(artist_id):
    meta = sp.artist(artist_id)
    return [meta['popularity'], meta['followers']['total']]

def getTrackFeatures(track_id):
    track = "NONE"
    while True:
        try:
            meta = sp.track(track_id)
            features = sp.audio_features(track_id)
            audio_analysis = sp.audio_analysis(track_id)

            # meta
            name = meta['name']
            artist_name = meta['album']['artists'][0]['name']
            release_date = meta['album']['release_date']
            if len(release_date) == 4:
                release_date = release_date + "-01-01"
            popularity = meta['popularity']
            artists_features = getAllArtistsFollowersFromTrack(track_id)
            artist_popularity = artists_features[0]
            artist_followers = artists_features[1]
            number_of_artists = artists_features[2]
            list_of_artists = artists_features[3]

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
            key = features[0]['key']
            mode = features[0]['mode']
            valence = features[0]['valence']
            duration_ms = meta['duration_ms']
            lead_artist_id = list_of_artists[0]
            lead_artist_name = sa.getArtistName(lead_artist_id)
            sections = len(audio_analysis['sections'])

            track = [name, artist_name, track_id, danceability, energy, loudness, mode,
                     speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature,
                     sections, 0, "", popularity, release_date, 0, artist_popularity, artist_followers,
                     number_of_artists,
                     list_of_artists, key, lead_artist_id, lead_artist_name]

            break
        except spotipy.SpotifyException as e:
            print(e)
            break
        except Exception as e:
            continue

    return track
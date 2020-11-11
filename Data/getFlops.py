import spotipy
import pandas as pd
import SpotipyAPITest as spot
import os
import ast

from spotipy.oauth2 import SpotifyClientCredentials
os.environ['SPOTIPY_CLIENT_ID'] = '0352b9dc8c1b44f69aeee6cae24f0f53'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'c4003dba4d564ccaaaa23c1044f34b92'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Set ipython's max row display
pd.set_option('display.max_row', 1000)

'''Searching for all individual artists from billboard dataset
 and getting more of their songs released after 2020 if it is not the billboard dataset'''

def getTracksFromArtistName(artist, offset_factor):
    results = sp.search(q="artist:" + artist + " year:2000-2020 NOT remix", limit=50, offset=50*offset_factor)
    items = results["tracks"]["items"]
    id = "NONE"
    if (len(items) > 0):
        id = [item["id"] for item in items] #was items[0]["id"]
    return id
#print(getTrackFromArtistName("Taylor Swift", 0))

#Get unique artists in list from billboard
df = pd.read_csv("CSV-files/OLD_FILES/billboard-spotify-data-org-key.csv")

#Dropping duplicate entries and artists that does not have originals
#dup = df[df.duplicated(['song_id'], keep=False)]
#print(dup['name'], dup['chart_date'])
df.drop(columns=['length'])
df.drop_duplicates(subset=['song_id'], inplace=True)
df.drop(df[df.artist == "Various Artists"].index, inplace=True)
df.drop(df[df.artist == "Glee Cast"].index, inplace=True)
print("Number of songs in dataset: " + str(len(df.index)))

artists = df.artist.unique()
print("Number of unique artists in dataset: " + str(len(artists))) #1292 unique artists after removing "Various Artists" and "Glee Cast"

df2 = pd.DataFrame({'artist':df.artist.unique()})
df2['song_ids'] = [list(set(df['song_id'].loc[df['artist'] == x['artist']]))
    for _, x in df2.iterrows()]
df2['song_names'] = [list(set(df['name'].loc[df['artist'] == x['artist']]))
    for _, x in df2.iterrows()]
#print(df2.loc[100])

df2['length'] = df2['song_ids'].str.len()
sort_by_len = df2.sort_values('length', ascending=False)
#print(sort_by_len.head(n=50))
#print(df2.columns)

#Add features target=0, chart_date="", weeks=""
def getFlopsForDataset(dframe):
    counter = 0
    data_count=0
    flops = []
    missing_songs = 0
    for i, row in dframe.iterrows():
        counter += 1
        number_of_hits = row['length']
        hits = row['song_ids']
        artist = row['artist']
        hits_names = row['song_names']
        songs_until_next_search = 0
        number_of_flops = 0
        songs_from_search = []
        offset = 0
        artist_flops = []
        artist_flops_name = []
        while number_of_flops < number_of_hits + missing_songs:
            songs_until_next_search = songs_until_next_search % 50
            if songs_until_next_search == 0:
                songs_from_search = getTracksFromArtistName(artist, offset)
                print(len(songs_from_search))
                offset += 1
                if songs_from_search == "NONE":
                    print("No more songs from this artist")
                    break
            if songs_from_search[songs_until_next_search] not in hits and songs_from_search[songs_until_next_search]\
                    not in artist_flops:
                #Legg til låt i datasett
                track = spot.getTrackFeatures(songs_from_search[songs_until_next_search])
                if track[0] not in artist_flops_name and track[0] not in hits_names:
                    data_count += 1
                    artist_flops.append(track[2]) #adding song_id to artist_flops
                    artist_flops_name.append(track[0])
                    flops.append(track)
                    number_of_flops += 1
                    print("Artist #", counter, "Flop #", data_count, ": ", artist, " (with ", number_of_hits, " hit(s)) has flop track ", track[0], " as flop#",
                          number_of_flops, ". songs_until_next_search:", songs_until_next_search)
            songs_until_next_search += 1
            if len(songs_from_search) < 50 and songs_until_next_search >= len(songs_from_search):
                missing_songs += (number_of_hits - number_of_flops)
                print("break with missing songs:", missing_songs)
                break
        if number_of_flops == number_of_hits + missing_songs:
            missing_songs = 0
    return flops

from pathlib import Path
data_folder = Path("CSV-files")
writeFile = "billboardwithflops111020.csv"
writePath = data_folder / writeFile
flop_list = getFlopsForDataset(df2)
flops = pd.DataFrame(flop_list, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key"])
df = df.append(flops)
df.to_csv(writeFile, index=False, header=True, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key"])

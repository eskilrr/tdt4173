import spotipy
import pandas as pd
from Data import SpotipyAPITest as spot
import os
import Data.searchForArtistAlbums as sa
from spotipy.oauth2 import SpotifyClientCredentials
os.environ['SPOTIPY_CLIENT_ID'] = '0352b9dc8c1b44f69aeee6cae24f0f53'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'c4003dba4d564ccaaaa23c1044f34b92'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Set ipython's max row display
#pd.set_option('display.max_row', 1000)

'''Searching for all individual artists from billboard dataset
 and getting more of their songs released after 2020 if it is not the billboard dataset'''

def getTracksFromArtistName(artist, offset_factor):
    results = sp.search(q="artist:" + artist + " year:2000-2020 NOT Remix NOT Live NOT Acoustic", limit=50, offset=50*offset_factor)
    items = results["tracks"]["items"]
    id = "NONE"
    if (len(items) > 0):
        id = [item["id"] for item in items] #was items[0]["id"]
    return id

#Get unique artists in list from billboard
df = pd.read_csv("CSV-files/OLD_FILES/billboard-hits-2000-2020v3.csv")

#Dropping duplicate entries and artists that does not have originals
df.drop_duplicates(subset=['song_id'], inplace=True)
df.drop(df[df.artist == "Glee Cast"].index, inplace=True)
print("Number of songs in dataset: " + str(len(df.index)))

df['aid'] = df['lead_artist_name'] + "|" + df['artist_id']
artists = df.artist_id.unique()
df2 = pd.DataFrame({'aid': df.aid.unique()})
df2 = pd.DataFrame(df2.aid.str.split('|').tolist(),
                                 columns = ['artist','artist_id'])

df2.drop_duplicates(subset=['artist_id'], inplace=True)
print("Number of unique artists in dataset: " + str(len(artists))) #1292 unique artists after removing "Various Artists" and "Glee Cast"

df2['song_ids'] = [list(set(df['song_id'].loc[df['artist'] == x['artist']]))
    for _, x in df2.iterrows()]
df2['song_names'] = [list(set(df['name'].loc[df['artist'] == x['artist']]))
    for _, x in df2.iterrows()]
df2['song_ids'] = [list(set(df['song_id'].loc[df['artist'] == x['artist']]))
    for _, x in df2.iterrows()]

df2['length'] = df2['song_ids'].str.len()

df3 = pd.concat([df['song_id'], df['name']], axis=1, keys=["song_id", "name"])
del df['aid']

def getFlopsForDataset(dframe, dataf, dataf3):
    c = ["name", "artist", "song_id", "danceability", "energy", "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key", "artist_id",
                                                            "lead_artist_name"]
    counter = 0
    data_count = 0
    missing_songs = 0
    for i, row in dframe.iterrows():
        counter += 1
        number_of_hits = row['length']
        albums_to_fetch = min(int(number_of_hits/2)+10, 50)
        artist_id = row['artist_id']
        artist = row['artist']
        song_index = 0
        number_of_flops = 0
        songs_from_search = sa.getCatalogueFromArtist(artist_id, albums_to_fetch)
        l = len(songs_from_search[0])
        print(l)
        while number_of_flops < number_of_hits + missing_songs:
            if song_index >= l:
                missing_songs += (number_of_hits - number_of_flops)
                print("No more songs from", artist, ". Missing flops: ", missing_songs)
                break
            #Fetching data from song_id if song_id is not already in dataset
            if songs_from_search[0][song_index] not in dataf3.values and \
                    songs_from_search[1][song_index] not in dataf3.values:
                track = spot.getTrackFeatures(songs_from_search[0][song_index])
                # Only add song if title not in dataset and the artist_id matches
                if track != "NONE":
                    data_count += 1
                    todf3 = [[track[2], track[0]]]    #smaller dataframe for faster search
                    dataf3 = dataf3.append(pd.DataFrame(todf3, columns=['id', 'name']))
                    dataf = dataf.append(pd.DataFrame([track], columns=c))
                    number_of_flops += 1
                    print("Artist #", counter, "Flop #", data_count, ": ", artist, " (with ", number_of_hits,
                          " hit(s)) has flop track ", track[0], " as flop#",
                          number_of_flops, ". songs_until_next_search:", song_index, "ref: ", track[2])
            song_index += 1
        if number_of_flops == number_of_hits + missing_songs:
            missing_songs = 0
    return dataf

from pathlib import Path
data_folder = Path("CSV-files")
writeFile = "billboard-hits-flops-raw.csv"
writePath = data_folder / writeFile
new_df = getFlopsForDataset(df2, df, df3)
print(new_df)
new_df.to_csv(writeFile, index=False, header=True, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key", "artist_id",
                                                        "lead_artist_name"])

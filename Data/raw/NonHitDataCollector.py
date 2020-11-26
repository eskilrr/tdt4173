import spotipy
import pandas as pd
from Data.raw import SpotifyDataFromTracks as spot
import os
import Data.raw.SpotifyTracksFromArtist as sa
from spotipy.oauth2 import SpotifyClientCredentials
os.environ['SPOTIPY_CLIENT_ID'] = '0352b9dc8c1b44f69aeee6cae24f0f53'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'c4003dba4d564ccaaaa23c1044f34b92'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
import datetime as dt

path = "/Users/eivindrebnord/Development/tdt4173/Data/raw/"



#Cleaning hit song data from Billboard
billboard = pd.read_csv(path + "billboard.csv")

for i, row in billboard.iterrows():
    if len(row['release_date'])==4:
        #print(row['release_date'])
        billboard.at[i, 'release_date'] = row['release_date'] + "-01-01"
        continue
print(str(len(billboard)))
billboard['release_date'] = pd.to_datetime(billboard['release_date'], format='%Y-%m-%d').dt.date
billboard['release_year'] = pd.to_datetime(billboard['release_date']).dt.year
billboard['chart_year'] = pd.to_datetime(billboard['chart_date']).dt.year
billboard.drop(billboard[billboard.release_year > billboard.chart_year].index, inplace=True)
billboard.drop(billboard[billboard['artist'] == "Glee Cast"].index, inplace=True)
billboard = billboard.sort_values(by=['release_date'], ascending=False)
billboard = billboard.reset_index(drop=True)

df = billboard
df.drop(df[df.release_year < 2000].index, inplace=True)
#Dropping duplicate entries and artists that does not have originals
df.drop_duplicates(subset=['song_id'], inplace=True)
print("Number of songs in dataset: " + str(len(df.index)))

#Get unique artists in list from billboard
df['aid'] = df['lead_artist_name'] + "|" + df['artist_id']
df['weeksdate'] = df['chart_date'].apply(str) + "|" + df['weeks'].apply(str) #include chart dates with weeks for each artist
artists = df.artist_id.unique()
df2 = pd.DataFrame({'aid': df.aid.unique()})
df2 = pd.DataFrame(df2.aid.str.split('|').tolist(),
                                 columns = ['artist','artist_id'])

df2.drop_duplicates(subset=['artist_id'], inplace=True)
print("Number of unique artists in dataset: " + str(len(artists)))

df2['song_ids'] = [list(set(df['song_id'].loc[df['artist'] == x['artist']]))
    for _, x in df2.iterrows()]
df2['song_names'] = [list(set(df['name'].loc[df['artist'] == x['artist']]))
    for _, x in df2.iterrows()]
df2['weeksdates'] = [list(set(df['weeksdate'].loc[df['artist'] == x['artist']]))
    for _, x in df2.iterrows()]
df2['length'] = df2['song_ids'].str.len()
df2.to_csv(path + "artist_dataframe.csv", index=False, header=True, columns=["artist", "artist_id", "song_ids", "song_names", "length",
                                                                  "weeksdates"])
#df2 = pd.read_csv("artist_dataframe.csv")
df2 = df2.iloc[889:] #start from specific artist
df = pd.read_csv(path + "allFlops.csv") #read allFlops as df from last saved state

#Make smaller dataframe for faster search when checking if track already exists in dataset in method under
df3 = pd.concat([df['song_id'], df['name']], axis=1, keys=["song_id", "name"])

'''Searching for all the entire catalogue for all artists included in the hit dataset. This method does not include
   tracks already included in the hit dataset.'''

def getFlopsForDataset(dframe, dataf, dataf3):
    c = ["name", "artist", "song_id", "danceability", "energy", "loudness", "mode", "speechiness", "acousticness",
            "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature", "sections",
            "target", "chart_date", "popularity", "release_date", "weeks", "artist_popularity", "artist_followers",
            "number_of_artists", "list_of_artists", "key", "artist_id", "lead_artist_name"]
    counter = 0
    data_count = 1
    missing_songs = 0
    #Iterates through all the artists in the hit dataframe
    for i, row in dframe.iterrows():
        #Parses a list of [release date, weeks] for all the hits of the artist
        weeksdates = sorted([item.split('|') for item in row['weeksdates']],
                            key=lambda x: dt.datetime.strptime(x[0], "%Y-%m-%d").date(), reverse=True)
        counter += 1
        number_of_hits = row['length']
        artist_id = row['artist_id']
        artist = row['artist']
        song_index = 0
        number_of_flops = 0
        songs_from_search = sa.getAllUniqueArtistSongs(artist_id)
        l = len(songs_from_search[0])
        print(l)
        while True:
            if data_count % 100 == 0:
                dataf.to_csv(path + "allFlops.csv", index=False, header=True,
                       columns=c)
                print("Saved file")
            if song_index >= l:
                missing_songs += (number_of_hits - number_of_flops)
                print("No more songs from", artist, ". Missing flops: ", missing_songs)
                break
            #Fetching data from song_id if song_id or song_name is not already in dataset
            if songs_from_search[0][song_index] not in dataf3.values and \
                    songs_from_search[1][song_index] not in dataf3.values:
                track = spot.getTrackFeatures(songs_from_search[0][song_index])
                # Only add song if title not in dataset and the artist_id matches
                if track != "NONE" and track[-2] == artist_id:
                    r_date = track[19]
                    for h in weeksdates:
                        if dt.datetime.strptime(h[0], "%Y-%m-%d").date() <= dt.datetime.strptime(r_date, "%Y-%m-%d").date():
                            track[20] = h[1] #weeks is set to the number of weeks for the most recent hit
                            break
                    data_count += 1
                    todf3 = [[track[2], track[0]]]    #smaller dataframe for faster search
                    dataf3 = dataf3.append(pd.DataFrame(todf3, columns=['id', 'name']))
                    dataf = dataf.append(pd.DataFrame([track], columns=c))
                    number_of_flops += 1
                    print("Artist #", counter, "Flop #", data_count, ": ", artist, " (with ", number_of_hits,
                          " hit(s)) has flop track ", track[0], " as flop#",
                          number_of_flops, ". songs_until_next_search:", song_index, "ref: ", track[2])
            song_index += 1
    return dataf

from pathlib import Path
data_folder = Path(path)
writeFile = "allFlopsFinished.csv"
writePath = data_folder / writeFile
new_df = getFlopsForDataset(df2, df, df3)
new_df.to_csv(writeFile, index=False, header=True, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key", "artist_id",
                                                        "lead_artist_name"])

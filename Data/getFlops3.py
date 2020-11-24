import spotipy
import pandas as pd
import Data.SpotipyAPITest as spot
import os

from spotipy.oauth2 import SpotifyClientCredentials
os.environ['SPOTIPY_CLIENT_ID'] = '0352b9dc8c1b44f69aeee6cae24f0f53'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'c4003dba4d564ccaaaa23c1044f34b92'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Set ipython's max row display
#pd.set_option('display.max_row', 1000)

'''Searching for all individual artists from billboard dataset
 and getting more of their songs released after 2020 if it is not the billboard dataset'''

def getTracksFromArtistName(artist, offset_factor):
    id = "NONE"
    try:
        results = sp.search(q="artist:" + artist + " year:2000-2020 NOT remix NOT acoustic NOT live", limit=50, offset=50*offset_factor)
        items = results["tracks"]["items"]
        if len(items) > 0:
            id = [item["id"] for item in items] #was items[0]["id"]
    except Exception as e:
        return id
    return id
#print(getTrackFromArtistName("Taylor Swift", 0))

#Get unique artists in list from billboard
df = pd.read_csv("billboard.csv")

#Dropping duplicate entries and artists that does not have originals
df.drop_duplicates(subset=['song_id'], inplace=True)
#df.drop(df[df.artist == "Various Artists"].index, inplace=True)
#df.drop(df[df.artist == "Glee Cast"].index, inplace=True)
print("Number of songs in dataset: " + str(len(df.index)))

df['aid'] = df['lead_artist_name'] + "|" + df['artist_id']
df2 = pd.DataFrame({'aid': df.aid.unique()})
df2 = pd.DataFrame(df2.aid.str.split('|').tolist(),
                                 columns = ['artist','artist_id'])
df2.drop_duplicates(subset=['artist_id'], inplace=True)
print("Number of unique artists in dataset: " + str(len(df2)))

df2['song_ids'] = [list(set(df['song_id'].loc[df['lead_artist_name'] == x['artist']]))
    for _, x in df2.iterrows()]
df2['song_names'] = [list(set(df['name'].loc[df['lead_artist_name'] == x['artist']]))
    for _, x in df2.iterrows()]

df2['length'] = df2['song_ids'].str.len()
df3 = pd.concat([df['song_id'], df['name']], axis=1, keys=["song_id", "name"])
del df['aid']

#sort_by_len = df2.sort_values('length', ascending=False)
#print(sort_by_len.head(n=50))
#print(df2.columns)

#Add features target=0, chart_date="", weeks=""
def getFlopsForDataset(dframe):
    counter = 0
    data_count=0
    flops = []
    missing_songs = 0
    for i, row in dframe.iterrows():
        if data_count > 7615:
            return flops
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
        found_any = True
        while number_of_flops < number_of_hits + missing_songs:
            songs_until_next_search = songs_until_next_search % 50
            if songs_until_next_search == 0:
                if not found_any:
                    missing_songs += (number_of_hits - number_of_flops)
                    print("Didn't find more flops last 50 songs for", artist, ". Missing flops: ", missing_songs)
                    break
                songs_from_search = getTracksFromArtistName(artist, offset)
                found_any = False
                print(len(songs_from_search))
                offset += 1
                if songs_from_search == "NONE":
                    missing_songs += (number_of_hits - number_of_flops)
                    print("No more songs from", artist, ". Missing flops: ", missing_songs)
                    break
            if songs_from_search[songs_until_next_search] not in hits and songs_from_search[songs_until_next_search]\
                    not in artist_flops:
                #Legg til låt i datasett
                track = spot.getTrackFeatures(songs_from_search[songs_until_next_search])
                song_name = track[0].split(" (")[0] #name of song without featuring
                #print(song_name, hits_names)
                #print(row)
                if song_name not in artist_flops_name and (not any(song_name in x for x in hits_names)) and \
                        track[-2] == row['artist_id']:
                    data_count += 1
                    found_any = True
                    artist_flops.append(track[2]) #adding song_id to artist_flops
                    artist_flops_name.append(track[0]) #adding song name
                    flops.append(track)
                    number_of_flops += 1
                    print("Artist #", counter, "Flop #", data_count, ": ", artist, " (with ", number_of_hits, " hit(s)) has flop track ", track[0], " as flop#",
                          number_of_flops, ". songs_until_next_search:", songs_until_next_search)
            songs_until_next_search += 1
            if len(songs_from_search) < 50 and songs_until_next_search >= len(songs_from_search):
                missing_songs += (number_of_hits - number_of_flops)
                print("Break with missing songs:", missing_songs)
                break
        if number_of_flops == number_of_hits + missing_songs:
            missing_songs = 0
    return flops

from pathlib import Path
data_folder = Path("CSV-files")
writeFile = "billboardwithflops112320.csv"
writePath = data_folder / writeFile
flop_list = getFlopsForDataset(df2)
flops = pd.DataFrame(flop_list, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key", "artist_id",
                                                        "lead_artist_name"])
df = df.append(flops)
df.to_csv(writeFile, index=False, header=True, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key", "artist_id",
                                                        "lead_artist_name"])

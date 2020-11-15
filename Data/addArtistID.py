import spotipy
import pandas as pd
import SpotipyAPITest as spot
import os
import ast
writeFile = "billboard-hits-2000-2020v2.csv"
#Get unique artists in list from billboard
df = pd.read_csv("CSV-files/OLD_FILES/billboard-hits-2000-2020.csv")
df['list_of_artists'] = df['list_of_artists'].apply(ast.literal_eval)
df['artist_id'] = df['list_of_artists'].str[0]
#df.loc[:, 'artist_id'] = df.list_of_artists.map(lambda x: x[0])

df.to_csv(writeFile, index=False, header=True, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key", "artist_id"])


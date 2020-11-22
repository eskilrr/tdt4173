
from datetime import datetime
import spotipy
import billboard
import re
from Data import SpotipyAPITest as spot
from pathlib import Path
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.model_selection import train_test_split
import time
import pandas as pd
#import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
cid = "b3c5b350c6cb43c2bdb403eb3b896eba"
secret = "fa1aa37ba9c943d3b4e2cadc8fd4818f"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTrackIdFromBillboard(name, artist):
    results = sp.search(q="track:" + name + " artist:" + artist)
    items = results["tracks"]["items"]
    id = "NONE"
    if (len(items) > 0):
        id = items[0]["id"]
    return id


def getChartDataFrame(chart, fullDataFrame):
    tracks = []
    for entry in chart.entries:
        #print(entry.title)
        artists = re.split(' & | x | Featuring | With |, ', str(entry.artist).replace(entry.title + " ", ""))
        #print(artists)
        id = getTrackIdFromBillboard(entry.title, artists[0])

        if (id != "NONE"):
            if (artists[0] in fullDataFrame.values) and (not any(dic['artist'] == artists[0] for dic in tracks)):
                fullDataFrame.loc[fullDataFrame['artist'] == artists[0], 'weeks'] += 1
            if (id not in fullDataFrame.values) and (entry.isNew):
                track = spot.getTrackFeatures(id)
                track["chart_date"] = datetime.strptime(chart.date, '%Y-%m-%d').date()
                tracks.append(track)
    df = pd.DataFrame(tracks)
    fullDataFrame = fullDataFrame.append(df)
    return fullDataFrame


def gatherBillboardData(dataf):

    chart = billboard.ChartData('hot-100')
    chart.previousDate = "2002-07-06"
    i = 0
    fullDataFrame = dataf

    '''pd.DataFrame(columns = ["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key"])'''
    start = time.time()
    while (chart.previousDate):
        #start = time.clock()
        print(chart.previousDate)
        fullDataFrame = getChartDataFrame(chart, fullDataFrame)
        chart = billboard.ChartData('hot-100', chart.previousDate)
        #end = time.clock()
        #print("total time: " + str(end-start))
        i += 1
        if (i == 180): #was 960
            break
        if (i == 480):
            print("halveis")
    end = time.time()
    print("total time: " + str(end-start))
    return fullDataFrame
data_folder = Path("CSV-files")
writeFile = "billboard-hits-2000-2020.csv"
writePath = data_folder / writeFile

almost = pd.read_csv('CSV-files/OLD_FILES/billboardv2.csv')

df = gatherBillboardData(almost)
df.to_csv(writeFile, index=False, header=True, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key"])



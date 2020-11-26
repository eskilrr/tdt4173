
from datetime import datetime
import spotipy
import billboard
import re
from Data.raw import SpotifyDataFromTracks as spot
from pathlib import Path
import time
import pandas as pd
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
        artists = re.split(' & | x | Featuring | With |, ', str(entry.artist).replace(entry.title + " ", ""))
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


def gatherBillboardData():

    chart = billboard.ChartData('hot-100')
    chart.previousDate = "2002-07-06"
    i = 0
    fullDataFrame = pd.DataFrame(columns = ["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key"])
    start = time.time()
    while (chart.previousDate):
        print(chart.previousDate)
        fullDataFrame = getChartDataFrame(chart, fullDataFrame)
        chart = billboard.ChartData('hot-100', chart.previousDate)
        i += 1
        if (i == 960): #Collecting data from the last 960 weeks
            break
        if (i == 480):
            print("halveis")
    end = time.time()
    print("total time: " + str(end-start))
    return fullDataFrame
data_folder = Path("CSV-files")
writeFile = "billboard.csv"
writePath = data_folder / writeFile

df = gatherBillboardData()
df.to_csv(writeFile, index=False, header=True, columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key"])



import pandas as pd

#Balancing our dataset with 50/50 hits/flops for each year from 2000-2020
new_df2 = pd.DataFrame(columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key", "artist_id",
                                                        "lead_artist_name", "release_year", "chart_year"])
allRecs = pd.read_csv("../raw/allFlops.csv")
allRecs['release_date'] = pd.to_datetime(allRecs['release_date'], format='%Y-%m-%d').dt.date
allRecs['release_year'] = pd.to_datetime(allRecs['release_date']).dt.year
billboard = allRecs[allRecs['target'] == 1]
flops = allRecs[allRecs['target'] == 0]
for i in range(21):
    print("Year: ", i, str(len(billboard[billboard['release_year'] == 2000 + i])))

    i_hits = billboard[billboard['release_year'] == 2000 + i]
    i_flops = flops[flops['release_year'] == 2000 + i]
    n_hits = len(i_hits)
    n_flops = len(i_flops)
    print(n_hits, n_flops)
    smallest_n = min(n_hits, n_flops)
    print(smallest_n)
    new_df2 = new_df2.append(billboard[billboard['release_year'] == 2000 + i].sample(n=smallest_n, random_state=1))
    new_df2 = new_df2.append(flops[flops['release_year'] == 2000 + i].sample(n=smallest_n, random_state=1))

print(str(len(new_df2)))
new_df2.to_csv("balanced.csv", index=False, header=True)
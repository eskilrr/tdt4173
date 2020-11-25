import pandas as pd
'''If artist of flop song is listed as one of the artists of a billboard song,
the 'weeks' feature of the flop songs should be the latest recorded number of weeks this artist
had on billboard up to the date of the release of the flop song'''

flops = pd.read_csv("flops112320.csv")
billboard = pd.read_csv("billboard.csv")
'''
for i, row in billboard.iterrows():
    if len(row['release_date'])==4:
        #print(row['release_date'])
        billboard.at[i, 'release_date'] = row['release_date'] + "-01-01"
        continue
'''
print(str(len(billboard)))
billboard['release_date'] = pd.to_datetime(billboard['release_date'], format='%Y-%m-%d').dt.date
billboard['release_year'] = pd.to_datetime(billboard['release_date']).dt.year
billboard['chart_year'] = pd.to_datetime(billboard['chart_date']).dt.year
billboard.drop(billboard[billboard.release_year > billboard.chart_year].index, inplace=True)
billboard = billboard.sort_values(by=['release_date'], ascending=False)
billboard = billboard.reset_index(drop=True)
print(str(len(billboard)))

flops['release_date'] = pd.to_datetime(flops['release_date'], format='%Y-%m-%d').dt.date
flops = flops.sort_values(by=['release_date'], ascending=False)
flops = flops.reset_index(drop=True)
flops['release_year'] = pd.to_datetime(flops['release_date']).dt.year
'''
#Update index hered
count = 0
for x, flop in flops.iterrows():
    count += 1
    if count%100==0:
        print(count)
    #weeks = [0]
    for y, hit in billboard.iterrows():
        #Continue looping if date of flop is older than hit release date
        if flop['release_date'] < hit['release_date']:
            continue

        if flop['lead_artist_name'] in hit.values:
            flops.at[x, 'weeks'] = hit['weeks']
            #weeks.append(hit['weeks'])
            break

    #flops.at[x, 'weeks'] = max(weeks)

flops.to_csv("flops112320_weeks.csv", index=False, header=True)
'''
new_df2 = pd.DataFrame(columns=["name", "artist", "song_id", "danceability", "energy",
                                                             "loudness", "mode", "speechiness", "acousticness",
                                                             "instrumentalness", "liveness", "valence", "tempo",
                                                             "duration_ms", "time_signature", "sections",
                                                             "target", "chart_date", "popularity", "release_date",
                                                             "weeks", "artist_popularity", "artist_followers",
                                                             "number_of_artists", "list_of_artists", "key", "artist_id",
                                                        "lead_artist_name", "release_year", "chart_year"])

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
new_df2.to_csv("new_df2.csv", index=False, header=True)
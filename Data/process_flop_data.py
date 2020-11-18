import pandas as pd
import ast
'''If artist of flop song is listed as one of the artists of a billboard song,
the 'weeks' feature of the flop songs should be the latest recorded number of weeks this artist
had on billboard up to the date of the release of the flop song'''

flops = pd.read_csv("CSV-files/flops.csv")
billboard = pd.read_csv("billboard.csv")

flops['release_date'] = pd.to_datetime(flops['release_date'], format='%Y-%m-%d').dt.date
flops = flops.sort_values(by=['weeks'], ascending=False)
flops = flops.reset_index(drop=True)

for i, row in billboard.iterrows():
    if len(row['release_date'])==4:
        #print(row['release_date'])
        billboard.at[i, 'release_date'] = row['release_date'] + "-01-01"
        continue
    #billboard.at[i, 'release_date'] = row['release_date'].replace(".", "-")
billboard['release_date'] = pd.to_datetime(billboard['release_date'], format='%Y-%m-%d').dt.date
billboard = billboard.sort_values(by=['release_date'], ascending=False)
billboard = billboard.reset_index(drop=True)

#Update index here
#flops.insert(9, "Weeks")
count = 0
for x, flop in flops.iterrows():
    count += 1
    if count%100==0:
        print(count)
    weeks = [0]
    for y, hit in billboard.iterrows():
        #print(y, hit['release_date'])
        #Continue looping if date of flop is older than hit release date
        if flop['release_date'] < hit['release_date']:
            #print(flop['release_date'], hit['release_date'])
            continue

        if flop['lead_artist_name'] in hit.values:
            weeks.append(hit['weeks'])
        '''
        #Set all number of weeks for
        fa = ast.literal_eval(flop['list_of_artists'])
        #print(fa)
        for flop_artist in fa:
            ha = ast.literal_eval(hit['list_of_artists'])
            for hit_artist in ha:
                if flop_artist == hit_artist:
                    #print(flop_artist, hit_artist, hit['weeks'])
                    weeks.append(hit['weeks'])
        '''
    flops.at[x, 'weeks'] = max(weeks)
    #print(flops.at[x, 'weeks'])

flops.to_csv("flops-weeks.csv", index=False, header=True)
#print(flops['weeks'])
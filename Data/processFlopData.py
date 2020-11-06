import pandas as pd

'''If artist of flop song is listed as one of the artists of a billboard song,
the 'weeks' feature of the flop songs should be the latest recorded number of weeks this artist
had on billboard up to the date of the release of the flop song'''

flops = pd.read_csv("CSV-files/flopdata-v1.csv")
billboard = pd.read_csv("CSV-files/billboard-spotify-data-org.csv")

flops['release_date'] = pd.to_datetime(flops['release_date'], format='%Y-%m-%d').dt.date
flops = flops.sort_values(by=['weeks'], ascending=False)

billboard['release_date'] = pd.to_datetime(billboard['release_date'], format='%Y-%m-%d').dt.date
billboard = billboard.sort_values(by=['release_date'], ascending=False)

#Update index here
#flops.insert(9, "Weeks")
count = 0
for x, flop in flops.iterrows():
    weeks = [0]
    for y, hit in billboard.iterrows():
        #Continue looping if date of flop is older than hit release date
        if flop['release_date'] < hit['release_date']:
            continue
        #Continue looping if artist does not match
        if flop['artists'] != hit['artists']:


        #Set all number of weeks for
        for flop_artist in flop['artists']:
            for hit_artist in hit['artists']:
                if(flop_artist==hit_artist):
                    weeks.append(hit['weeks'])
        flop['weeks']=max(weeks)


        #print('Index:', x)
        print(flop['release_date'], flop['name'], flop['artist'])
        count += 1
        if count==100:
            break

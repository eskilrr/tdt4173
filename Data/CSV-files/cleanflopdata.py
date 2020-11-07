import pandas as pd
import csv
from pathlib import Path
data_folder = Path("CSV-files")

'''Remove chorus_hit column, delete all hits, only keep none-hits (flops)'''

#flops = pd.read_csv("CSV-files/flopdata-v1.csv")
openFile = "flopdata-v1.csv"
openPath = openFile
writeFile = "flopdata-v2.csv"
writePath = writeFile
with open(openPath, "r") as source:
    rdr = csv.reader(source)
    with open(writePath, 'w', newline='') as result:
        wtr = csv.writer(result)
        counter = 0
        for r in rdr:
            counter+=1
            if counter == 1:
                continue
            if int(r[18]) == 1:
                continue
            wtr.writerow((r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13]
                          , r[15], r[17], r[18], r[19], r[20], r[21], r[22], r[23], r[24], r[25], r[26], r[27]))

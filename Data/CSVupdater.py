import SpotipyAPITest as sp
from csv import reader
from csv import writer
from pathlib import Path
data_folder = Path("CSV-files")
#files = ["60s", "70s", "80s", "90s"]


def add_column_in_csv(input_file, output_file, transform_row):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        counter = 0
        for row in csv_reader:
            counter += 1
            #if counter <= 3796:
            #    continue
            if counter == 1:
                features = ["chart_date", "duration_ms", "popularity", "release_date", "weeks", "artist_popularity", "artist_followers", "number_of_artists", "lsit_of_artists"]
                row.extend(features)
                csv_writer.writerow(row)
                continue
            if counter % 50 == 0:
                print(counter)
            # Pass the list / row in the transform function to add column text for this row
            transform_row(row, csv_reader.line_num)
            # Write the updated row / list to the output file
            csv_writer.writerow(row)

#Updating billboard-data.csv with more data
openFile = "flopdata_v0.csv"
writeFile = "flopdata-v1.csv"
openPath = data_folder / openFile
writePath = data_folder / writeFile
add_column_in_csv(openPath, writePath, lambda row, line_num: row.extend(
            sp.getExtraFeaturesFromTrack(row[2].rpartition(':')[2])))
print("Finished")

'''def updateCSV(inputFiles):
    for item in inputFiles:
        openFile = "dataset-of-" + item + ".csv"
        writeFile = "dataset-of-" + item + "v2.csv"
        openPath = data_folder / openFile
        writePath = data_folder / writeFile
        add_column_in_csv(openPath, writePath, lambda row, line_num: row.extend(
            sp.getAllArtistsFollowersFromTrack(row[2].rpartition(':')[2])))
    print("Finished")
'''

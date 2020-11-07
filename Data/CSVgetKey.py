import SpotipyAPITest as sp
from csv import reader
from csv import writer
from pathlib import Path
data_folder = Path("CSV-files")

def add_column_in_csv(input_file, output_file, transform_row):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj, delimiter=";")
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        counter = 0
        for row in csv_reader:
            counter += 1
            if counter == 1:
                features = ["key"]
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
openFile = "billboard-spotify-data-org.csv"
writeFile = "billboard-spotify-data-org-key.csv"
openPath = data_folder / openFile
writePath = data_folder / writeFile
add_column_in_csv(openPath, writePath, lambda row, line_num: row.extend(
            sp.getKey(row[2])))
print("Finished")


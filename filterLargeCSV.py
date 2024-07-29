# you do this step FIRST to generate the filtered file
#This program filters the cells of the large CSV files based on certain conditions

import csv
import json

#Function to filter the count CSV file and store its processed cells
def filter_count_csv(file_path, output_file_path, processed_indices_file):
    print(f"Filtering count file: {file_path}")
    
    with open(file_path, mode='r') as infile, open(output_file_path, mode='w', newline='') as outfile, open(processed_indices_file, mode='w') as processed_file:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        headers = next(reader)  #Read header
        writer.writerow(headers)  #Write header to the output file

        processed_indices = []
        for row_index, row in enumerate(reader):
            job1 = row[0]
            new_row = [job1]
            for col_index, cell in enumerate(row[1:], start=1):
                job2 = headers[col_index]
                #Print statement for testing, will crash vscode if used
                #print(f"Processing cell: Row header '{job1}', Column header '{job2}', Value: '{cell}'")
                
                #If the cells dont have these values then they are processed to the filtered versions, else they are left blank
                if cell != '' and cell not in ['0', '1', '2']:
                    new_row.append(cell)
                    processed_indices.append((row_index, col_index))
                else:
                    new_row.append('')
                    #Print statement for testing, will crash vscode if used
                    #print(f"Skipped cell: Row header '{job1}', Column header '{job2}', Value: '{cell}'")
            writer.writerow(new_row)
            
        json.dump(processed_indices, processed_file)
    
    print(f"Finished filtering count file: {file_path}")
    print("Finished saving the processed cells")

#Function to filter other CSV files based on the processed cells from the count CSV file
def filter_other_csv(file_paths, processed_indices_file):
    with open(processed_indices_file, 'r') as f:
        processed_indices = set(map(tuple, json.load(f)))  #Load processed cells as a set for quick lookup
    
    for file_path in file_paths:
        output_file_path = file_path.replace('.csv', '_filtered.csv')
        print(f"Filtering file: {file_path}")
        
        with open(file_path, mode='r') as infile, open(output_file_path, mode='w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            headers = next(reader)  #Read header
            writer.writerow(headers)  #Write header to the output file

            for row_index, row in enumerate(reader):
                job1 = row[0]
                new_row = [job1]
                for col_index, cell in enumerate(row[1:], start=1):
                    job2 = headers[col_index]
                    if (row_index, col_index) in processed_indices:
                        new_row.append(cell)
                        #Print statement for testing, will crash vscode if used
                        #print(f"Writing cell: Row header '{job1}', Column header '{job2}', Value: '{cell}'")
                    else:
                        new_row.append('')
                        #Print statement for testing, will crash vscode if used
                        #print(f"Skipped cell: Row header '{job1}', Column header '{job2}', Value: '{cell}'")
                writer.writerow(new_row)
        
        print(f"Finished filtering file: {file_path}")

#Define file paths
count_csv_file = 'count.csv'
count_filtered_file = 'count_filtered.csv'
processed_indices_file = 'processed_indices.json' #Used for the additional csv files

#Define other CSV files
# are they meant to be commented out???? lost man 
other_csv_files = [
    'mean.csv',
    'median.csv',
    'max.csv',
    'min.csv'
]

#Process the count CSV file
filter_count_csv(count_csv_file, count_filtered_file, processed_indices_file)

#Process other CSV files
filter_other_csv(other_csv_files, processed_indices_file)

print('all CSV files processed!')
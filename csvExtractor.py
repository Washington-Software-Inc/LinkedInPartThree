# you do this step SECOND to split the filtered file and view the contents within 
# note that the split csv files will not be in the correct format, so be wary of that! 
# you may want to note the number of parts that you want

#THIS CODE EXTRACTS VERY LARGE CSV FILES INTO SMALLER FILES JUST TO SEE ITS CONTENTS
#Note THAT THE EXTRACTED FILES WILL NOT BE ACCURATE TO THE LARGE ONE BECAUSE THEY GOT SPLIT AND DOES NOT REPRESENT THE ENTIRE FILE
import csv

#Define the path to the large CSV file: mean, median, max, min, count
#Put the CSV files you want to extract here
input_csv_file = 'mean_filtered.csv'

#Define the number of parts you want to split the file into
num_parts = 19

#Calculate the total number of rows and columns
print("Calculating the total number of rows and columns...")
with open(input_csv_file, 'r', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    total_rows = sum(1 for _ in f) + 1  #Add 1 to include the header row
    total_columns = len(header)
    
print(f"Total number of rows: {total_rows}")
print(f"Total number of columns: {total_columns}")

#Calculate rows per part
rows_per_part = total_rows // num_parts
remainder_rows = total_rows % num_parts

print(f"Rows per part: {rows_per_part}, with {remainder_rows} extra rows to distribute.")

#Split the CSV file into smaller parts
with open(input_csv_file, 'r', newline='') as infile:
    reader = csv.reader(infile)
    header = next(reader)  #Read the header

    part_number = 1
    row_count = 0
    current_part_rows = []

    #THIS IS THE NAME OF THE EXTRACTED FILES
    output_file = f'mean_filtered{part_number}.csv'
    outfile = open(output_file, 'w', newline='')
    writer = csv.writer(outfile)

    for row in reader:
        current_part_rows.append(row)
        row_count += 1

        if row_count >= (rows_per_part + (1 if remainder_rows > 0 else 0)):
            #Prepare column headers for this part
            column_headers = [row[0] for row in current_part_rows]
            writer.writerow([''] + column_headers)  #Write the updated header
            
            for current_row in current_part_rows:
                writer.writerow(current_row[:len(column_headers) + 1])  #Ensure row length matches header length
            
            outfile.close()  #Close the current file
            part_number += 1
            if part_number > num_parts:
                break
            
            #THIS IS THE NAME OF THE EXTRACTED FILES
            output_file = f'mean_filtered{part_number}.csv'
            outfile = open(output_file, 'w', newline='')
            writer = csv.writer(outfile)
            
            current_part_rows = []
            row_count = 0
            if remainder_rows > 0:
                remainder_rows -= 1

    #Write remaining rows if any
    if current_part_rows:
        column_headers = [row[0] for row in current_part_rows]
        writer.writerow([''] + column_headers)  #Write the updated header

        for current_row in current_part_rows:
            writer.writerow(current_row[:len(column_headers) + 1])  #Ensure row length matches header length

        outfile.close()  #Close the last file

print("CSV file splitting completed.")
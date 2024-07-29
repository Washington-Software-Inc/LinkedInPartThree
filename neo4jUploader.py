
# MAKE SURE THAT WHEN YOU'RE RUNNING THIS FILE, YOU NEED TO USE YOUR OWN USER AND PASS
# don't forget to edit those 

# r-0NKKqTidrr5Kcjjx_6WXzbXYVBhkLUBQL8t_RWWZo
# user: neo4j 
# pass: zkWps6edS7Z2b_kH04GZ7OkR4VbFEk3s5xoRfeiO6sM

#Part 3:
#This program here uploads the filtered CSV files to neo4j
import csv
from neo4j import GraphDatabase

#Function to read CSV files and process each cell
def read_and_process_csv(file_paths, value_type, process_cell_callback):
    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)  #Skips the header row (first row)

            #Process the remaining rows
            for row_index, row in enumerate(reader):
                job1 = row[0]  #First element in the row is the job title for this row
                for col_index, cell in enumerate(row[1:], start=1):  #Skip the first column (job titles)
                    job2 = headers[col_index]
                    if cell != '':  #Skip empty cells and cells with a single 0, 1, and 2
                        value = float(cell)  #Assuming cell contains a numeric value
                        process_cell_callback(job1, job2, value, value_type)
        print(f"Finished processing file: {file_path}")

#Function to create nodes and relationships in Neo4j
def upload_to_neo4j(driver, file_paths_with_types):
    def process_cell(job1, job2, value, value_type):
        with driver.session() as session:
            session.write_transaction(create_nodes_and_relationships, job1, job2, value, value_type)
        #Testing print statement below, may crash vscode if used 
        #print(f"Processed cell: {job1} -> {job2} with {value_type} value {value}")

    for file_paths, value_type in file_paths_with_types:
        read_and_process_csv(file_paths, value_type, process_cell)

#Transaction function to create nodes and relationships
def create_nodes_and_relationships(tx, job1, job2, value, value_type):
    query = f"""
    MERGE (job1:JobTitle {{title: $job1}})
    MERGE (job2:JobTitle {{title: $job2}})
    MERGE (job1)-[:TRANSITION {{type: '{value_type}', value: $value}}]->(job2)
    """
    tx.run(query, job1=job1, job2=job2, value=value)
    
    #Testing print statement below, may crash vscode if used 
    #print(f"Created nodes and relationship for: {job1} -> {job2} with {value_type} value {value}")

#Main function
def main():
    print("Starting the upload process...")
    
    #List of CSV file paths grouped by their type
    file_paths_with_types = [
        #For the filtered files
        #(['count_filtered.csv'], 'count')
        #(['mean_filtered.csv'], 'mean'),
        #(['median_filtered.csv'], 'median'),
        #(['max_filtered.csv'], 'max'),
        (['min_filtered.csv'], 'min'),
    ]
    
    #Connectting to Neo4j
    uri = "neo4j+s://70241113.databases.neo4j.io"  #Adjust this to your Neo4j URI
    user = "neo4j"  #Replace with your Neo4j username
    password = "r-0NKKqTidrr5Kcjjx_6WXzbXYVBhkLUBQL8t_RWWZo"  #Replace with your Neo4j password
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    print("Connected to Neo4j")

    #Calls function to Upload data to Neo4j (upload_to_neo4j -> create_nodes_and_relationships -> read_and_process_csv -> End)
    upload_to_neo4j(driver, file_paths_with_types)
    
    #Close the Neo4j driver
    driver.close()
    
    print("Finished the upload process. Yay!")

if __name__ == "__main__":
    main()
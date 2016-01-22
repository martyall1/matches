port = 8000

ip = "0.0.0.0"

#this is the number of comparisons a user must make before they are redirected to /finish
min_repetitions = 100

#this is the name of the csv file that will be downloaded from /data
csv_filename = "matches.csv"

#these are the names of the columns in the csv that will be downloaded from /data
csv_columns = ["decision_id", "contract_id", "is_match", "is_not_match", "pass"]  

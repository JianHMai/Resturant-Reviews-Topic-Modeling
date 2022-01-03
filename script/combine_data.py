import os
import csv

# Retrieve all locations of processed reviews
def get_locations():
    # List to hold location of all processed reviews
    file_locations = []

    # Yelp directory to search
    directory = "dataset/yelp/processed_reviews/"
    # Go through each Yelp file
    for filename in os.listdir(directory):
    # Find all files that end with CSV
	    if filename.endswith(".csv"):
			# Process each file
		    file_locations.append(os.path.join(directory, filename))
    # Google directory to search
    directory = "dataset/google/processed_reviews/"
    # Go through each Google file
    for filename in os.listdir(directory):
        # Find all files that end with CSV
        if filename.endswith(".csv"):
            # Process each file found
            file_locations.append(os.path.join(directory, filename))
    return file_locations

# Used to combine reviews
def combine_reviews(file_locations):
    # Location to save new combined CSV
    save_location = 'dataset/all_reviews_processed.csv'
    with open(save_location, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        # Header row 
        writer.writerow(["Date", "Resturant Name", "Rating","Review", 'Source'])
        # Go through each processed file location list
        for i in file_locations:
            source = -1
            # Used to retrieve resturant names for Yelp
            if("dataset/yelp/processed_reviews/" in i):
                resturant_name = i
                resturant_name = resturant_name.replace("dataset/yelp/processed_reviews/", "")
                resturant_name = resturant_name.replace("_processed.csv", "")
                resturant_name = resturant_name.replace("-", " ")
                # Capitalize names
                resturant_name = resturant_name.title()
                source = 0
            # Used to retrieve resturant names for Google
            if("dataset/google/processed_reviews/" in i):
                resturant_name = i
                resturant_name = resturant_name.replace("dataset/google/processed_reviews/", "")
                resturant_name = resturant_name.replace("_processed.csv", "")
                resturant_name = resturant_name.replace("-", " ")
                # Capitalize names
                resturant_name = resturant_name.title()
                source = 1
            # Open each process file
            with open(i, 'r', encoding='utf8') as csvfile:
                datareader = csv.reader(csvfile)
                # Skip header row
                next(datareader)
                for data in datareader:
                    # Depending on source write corresponding data and remove empty reviews
                    if source == 1 and data[3]:
                        writer.writerow([data[1], resturant_name, data[2], data[3], 'Google'])
                    elif source == 0 and data[2]:
                        writer.writerow([data[0], resturant_name, data[1], data[2], 'Yelp'])

file_locations = get_locations()
combine_reviews(file_locations)
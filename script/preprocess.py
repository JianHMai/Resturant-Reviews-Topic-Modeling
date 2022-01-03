import os
import pandas as pd
import csv
from nltk import word_tokenize
import string
from nltk.stem import WordNetLemmatizer
import nltk

# Function to process yelp data
def process_yelp_data(location, resturant_name):
	write_location = 'dataset/yelp/processed_reviews/' + resturant_name.replace("reviews.csv", "processed.csv")
	# Read scraped yelp data
	with open(location, 'r', encoding='utf8') as csvfile:
		datareader = csv.reader(csvfile)
		# Write CSV file in write location
		with open(write_location, 'w', newline='', encoding='utf8') as f:
			writer = csv.writer(f)
			# Writes the header rows
			writer.writerow(["date" ,"rating","review"])
			# Loop through each row
			for row in datareader:
				# Retrieve all data beyond the 3rd column
				review = row[2:]
				# String to hold reviews
				full_review = ""
				# Append data from other columns to full_review string
				for i in review:
						full_review = full_review + i
				# Remove all empty lines
				full_review = full_review.replace('\\n', " ")
				full_review = full_review.replace('\n', " ")
				full_review = full_review.replace('/', " ")
				# Remove any periods
				full_review = full_review.replace('.', " ")
				try:
					# Retrieve date
					date = row[0]
					# Retrieve rating
					rating = row[1]
					# Process the data
					data = NLP(full_review)
					if(rating.isnumeric()):
						# Write into new CSV
						writer.writerow([date, rating, data])
				except Exception as exc:
					print(write_location)
					print("row ====== : {}".format(row))
					print("review ====== : {}".format(review))
					print(exc)

# Function to process google data
def process_google_data(location, resturant_name):
		write_location = 'dataset/google/processed_reviews/' + resturant_name.replace(".csv", "_processed.csv")
		# Open scraped reviews data
		with open(location, 'r', encoding='utf8') as csvfile:
			datareader = csv.reader(csvfile)
			# Skip header row
			next(datareader)
			# Create processed csv
			with open(write_location, 'w', newline='', encoding='utf8') as f:
				writer = csv.writer(f)
				# Create header row
				writer.writerow(["author", "date", "rating","text"])
				for row in datareader:
					# Retrieve all reviews beyond 4th column
					review = row[3:]
					full_review = ""
					for i in review:
						full_review = full_review + i
						# Remove all empty lines
						full_review = full_review.replace('\\n', " ")
						full_review = full_review.replace('\n', " ")
						full_review = full_review.replace('/', " ")
						# Remove any periods
						full_review = full_review.replace('.', " ")
					# Holds author
					author = row[0]
					# Holds date
					date = row[1]
					# Hold rating
					rating = row[2]
					# Process data
					data = NLP(full_review)
					if(rating.strip().isnumeric()):
						# Write data to csv row
						writer.writerow([author, date, rating, data])
# Used to process data
def NLP(full_review):
	# Tokenize reivew
	tokens = word_tokenize(full_review)
	# Make all tokens lower case
	tokens = [token.lower() for token in tokens]
	# Remove all punctuation and -
	tokens = [token.strip(string.punctuation + '—') for token in tokens]
	stop_words = nltk.corpus.stopwords.words('english')
	# Remove stop words
	new_tokens = [word for word in tokens if word not in stop_words]
	tokens = new_tokens
	wordnet_lemmatizer = WordNetLemmatizer()
	# Lemmization of tokens
	tokens = [wordnet_lemmatizer.lemmatize(token) for token in tokens]
	# Strip empty tokens
	tokens = [token.strip() for token in tokens
			if token.strip()!=""]
	# Combine all tokens together
	all_reviews = " ".join(tokens)
	# Remove special characters
	return all_reviews.encode("ascii", errors="ignore").decode()

# Location to loop through Yelp reviews
# Go to folder
def process_yelp():
	print("Processing Yelp Review Data!!")
	directory = "dataset/yelp/reviews/"
	for filename in os.listdir(directory):
		# Find all files that end with CSV
		if filename.endswith(".csv"):
			# Process each file
			process_yelp_data(os.path.join(directory, filename), filename)

# Location to loop through Google reviews
# Go to folder
def process_google():
	print("Processing Google Review Data!!")
	directory = "dataset/google/reviews/"
	for filename in os.listdir(directory):
		# Find all files that end with CSV
		if filename.endswith(".csv"):
			# Process each file found
			process_google_data(os.path.join(directory, filename), filename)

process_google()
process_yelp()
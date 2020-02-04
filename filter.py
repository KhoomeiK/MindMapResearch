from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

import os, csv

from shutil import copy

BASE = '/Users/kamil/Desktop/MindMap/Research/MindMapResearch'
DATA_DIR = 'users'
DATA_DST = 'depressed_users'

# filter csv's which aren't actually depressed 
def filter_csvs():
	
	# initialize directory where the csv's are
	data_directory = os.path.join(BASE, DATA_DIR)
	
	# initialize directory where the scraped csv's will go
	new_directory = os.path.join(BASE, DATA_DST)

	# loop through each csv one by one only if it's a csv
	for filename in os.listdir(data_directory):
		depression_counts = 0.0
		total_depression_posts = 0.0
		
		# loop through each row of csv, only classify if it's depression subreddit comment
		with open(os.path.join(data_directory, filename), encoding='utf-8') as f:
			data = csv.reader(f, delimiter=',')
			next(data)
			
			# call classify() and add to depression counts if depressed
			for row in data:
				if row[0] == 'depression':
					total_depression_posts += 1
					depression_counts += classify(row[-1])
		
		# if depression_counts/csv_counts is >= .5, add to the depressed_users folder
		if total_depression_posts != 0 and (depression_counts/total_depression_posts) >= .5:
			copy(os.path.join(data_directory, filename), new_directory)

# get vader and use to classify
def classify(comment):
	# Create a SentimentIntensityAnalyzer object. 
	sid_obj = SentimentIntensityAnalyzer() 

	# polarity_scores method of SentimentIntensityAnalyzer 
	# oject gives a sentiment dictionary. 
	# which contains pos, neg, neu, and compound scores. 
	sentiment_dict = sid_obj.polarity_scores(comment) 

	if sentiment_dict['compound'] <= -0.05:
		return 1 
	return 0

def main():
	filter_csvs()

if __name__ == '__main__':
	main()
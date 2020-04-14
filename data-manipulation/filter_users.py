import os, csv
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

# filter csv's which aren't actually depressed 
def create_mappings(fnames, data):
	scores= {}
	total_depression_posts = 0.0
	total_posts = 0.0
	reg = 0.0
	vader_score = 0.0
	num_dep = 0
	# loop through each row of csv, only classify if it's depression subreddit comment

	# call classify() and add to depression counts if depressed
	for i in range(len(data)):
		print('Classifying {}\'s posts ({}/{})'.format(fnames[i], i, len(data)))
		isDep = False
		# if i == 26:
		# print(len(data[i])
		for index, row in data[i].iterrows():
			# index is the index of the row of the ith csv
			if len(row) > 0:
				if row[0] == 'depression': # might remove this and do classification on all
					total_depression_posts += 1.0
					if not isDep:
						num_dep += 1
						isDep = True
				if type(row[-1]) == type(''):
					vader_score += classify(row[-1])
					total_posts += 1.0
		# add to dict 
		reg = total_depression_posts/total_posts
		vader_score /= total_posts

		# dict which maps to regression score & vader score
		scores[fnames[i]] = [reg, vader_score]
	return scores, num_dep

# get vader and use to classify
def classify(comment):
	# Create a SentimentIntensityAnalyzer object. 
	sid_obj = SentimentIntensityAnalyzer() 

	# polarity_scores method of SentimentIntensityAnalyzer 
	# oject gives a sentiment dictionary. 
	# which contains pos, neg, neu, and compound scores. 
	sentiment_dict = sid_obj.polarity_scores(comment) 

	# return compound score [-1, 1]
	return sentiment_dict['compound']


	
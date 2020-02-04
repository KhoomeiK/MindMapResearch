import os, csv

import nltk, re
from nltk.corpus import stopwords

import word_category_counter

import sys

LIWC_DIR = "/Users/kamil/Desktop/MindMap/Research/MindMapResearch"
 
word_category_counter.load_dictionary(LIWC_DIR)

# have terminal options for csv's, subreddit(s), boolean for all messages or not
# have terminal 

BASE = '/Users/kamil/Desktop/MindMap/Research/MindMapResearch'
DATA_DIR_ALL = 'users'
DEPRESSED_DATA_DIR = 'depressed_users'

# METHOD: load_csvs
# @param: 
#	all_users: boolean value denoting whether csvs of all users should be scraped or just depressed
#				default value False
# @return: dictionary of filename : strings
def load_csvs(all_users=False, all_messages=True):
	data_directory = ""
	
	# build data_directory paths
	if(all_users):
		data_directory = os.path.join(BASE, DATA_DIR_ALL)
	else:
		data_directory = os.path.join(BASE, DEPRESSED_DATA_DIR)

	user_comments = {}

	# load every csv, one by one
	for filename in os.listdir(data_directory):
		user_comments[filename[:-4]] = load_single_csv(data_directory, filename, all_messages)

	return user_comments

# METHOD: load_single_csv
# input:
#	data_directory 
# 	a single csv
# 	optional: boolean if all messages or just messages from certain subreddit
	# optional: list containing subreddits to be scraped in particular
# output:
# 	list of strings containing the messages being scored
def load_single_csv(data_directory, filename, all_messages):
	messages = []

	# loop through each row of csv, only classify if it's depression subreddit comment
	with open(os.path.join(data_directory, filename), encoding='utf-8') as f:
		data = csv.reader(f, delimiter=',')
		next(data)
		
		# call classify() and add to depression counts if depressed
		for row in data:
			if not all_messages:
				if row[0] == 'depression':
					messages.append(row[-1])
			else:
				messages.append(row[-1])

	return messages

# METHOD: liwc_score_strings
# input:
# 	list of strings
# output:
# 	list of scores as determined by liwc
def liwc_score_strings(user_comments_dict):
	user_scores_dict = {}

	# each user
	for user in user_comments_dict.keys():
		
		# each user's comments 
		comments = user_comments_dict.get(user)
		
		user_scores = []
		
		# get scores as determined by liwc
		for comment in comments:

			# set stopwords, convert comment into sentence tokens
			stops = set(stopwords.words('english'))
			sentences = nltk.sent_tokenize(comment)
			words = []
			
			# convert each sentence into word tokens
			for sent in sentences:
			    words.extend([word for word in nltk.word_tokenize(sent) if not word in stops])

			# remove punctuation
			words = [re.search(r"\w+", word) for word in words]
			
			# convert back to word strings 
			words = [word.group() for word in words if word is not None]
			# print(words)

			# join words in sentence string
			text = " ".join(words)
			liwc_scores = word_category_counter.score_text(text)

			# avoid division by 0
			if len(set(words)) > 0:
				# add 1 (depressed) or 0 (not depressed) to the list if neg % > pos %
				score = -1
				if (liwc_scores['Negative Emotion'] + liwc_scores['Negations'] + liwc_scores['Sadness'] + liwc_scores['Death'])/len(set(words)) > (liwc_scores['Positive Emotion'] + liwc_scores['Optimism and energy'] + liwc_scores['Achievement'] + liwc_scores['Positive feelings'])/len(set(words)):
					score = 1
				else:
					score = 0
				user_scores.append(score)

		# add scores of user to user_scores_dict
		user_scores_dict[user] = user_scores

	# print(user_scores_dict)
	return user_scores_dict

# METHOD: convert_scores
# input: 
# 	list of liwc scores
# output:
# 	list of scores converted to binary classification of depression or not
def convert_scores(user_scores_dict):
	user_classified_dict = {}

	correct = 0
	# loop thru each of the users
	for user in user_scores_dict.keys():
		scores = user_scores_dict[user]
		net_avg = sum(scores)/len(scores)
		classification = -1
		if net_avg > 0.5:
			classification = 1
		else:
			classification = 0
		user_classified_dict[user] = classification
		correct += classification

	print(correct/len(user_scores_dict))
	return user_classified_dict

# METHOD: print_results()
# @param: user_classified_dict
	# dict of classifications by user
# @return: list of incorrect evaluations
# 
# prints overall percentage correct and returns dict of incorrect evaluations
# def print_results(user_classified_dict):

# 	for user in user_classified_dict.keys():
# 		user_classified_dict[user] = classifications
# 		if classification == 1:


# METHOD: classify_user
# input:
# 	list of binary classifications
# output:
# 	boolean output, if user is "depressed" or not as classified by liwc
# def classify_user():


# METHOD: run()
# input: N/A
# output: N/A
def run():
	user_comments_dict = load_csvs(all_messages=False)
	user_scores_dict = liwc_score_strings(user_comments_dict)
	print(user_scores_dict)
	user_classified_dict = convert_scores(user_scores_dict)


def main():
	run()

if __name__ == '__main__':
	main()
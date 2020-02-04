import os, csv, re, nltk, string, pickle

DATA_DIR = 'depressed_users'

def get_user_data(directory, filename):
	"""
	Parameters:
		directory: the directory to read from
		filename: the filename to read from

	Return Value:
		list containing reduced feature representation of a single Reddit user's comment activity
	"""
	results = []
	with open(os.path.join(directory, filename), encoding='utf-8') as f:
		data = csv.reader(f, delimiter=',')
		next(data)
		for row in data:
			tmp = {}
			tmp['subreddit'] = row[0]
			tmp['text'] = row[4]
			tmp['time'] = row[3]
			results.append(tmp)
	return results


def metrics(text, bigram_percent=0.1):
	"""
	Parameters:
		text: the text to analyze
		bigram_percent: the percentage of top bigrams to record from text

	Return Value:
		3-tuple containing corpus size, vocabulary_size, len of top `bigram_percent` bigrams
	"""
	return len(text), len(set(text)), len(nltk.FreqDist(nltk.bigrams(text)).most_common(int(bigram_percent * len(nltk.FreqDist(nltk.bigrams(text))))))


def get_user_post_metrics(posts, remove_punctuation=False, bigram_percent=0.1):
	"""
	Parameters:
		posts: a list of posts generated from the `get_user_data()` function
		remove_punctuation: whether to remove punctuation or not

	Return Value:
		2-tuple with the mini-corpus of a singular user's posts, and the metrics on that mini-corpus
	"""
	corpus = []
	for post in posts:
		val = nltk.word_tokenize(post['text'])
		if not remove_punctuation and post['text'] != '':
			corpus.extend(val)
		elif remove_punctuation and post['text'] != '':
			corpus.extend([v.translate(str.maketrans('', '', string.punctuation))
						   for v in val if v.translate(str.maketrans('', '', string.punctuation)) != ''])
	return corpus, metrics(corpus, bigram_percent)


def get_corpus_metrics(directory, remove_punctuation=False, bigram_percent=0.1):
	"""
	Parameters:
		directory: the directory of CSV files to analyze
		remove_punctuation: whether to remove punctuation or not

	Return Value:
		2-tuple consisting of the full corpus, and the metrics on the corpus
	"""
	corpus = []
	for filename in os.listdir(directory):
		val, _ = get_user_post_metrics(get_user_data(
			directory, filename), remove_punctuation)
		corpus.extend(val)
	return corpus, metrics(corpus, bigram_percent)


def save_binary(filename, item):
	"""
	Parameters:
		filename: the filename to save as
		item: the python variable to save in binary format
	"""
	with open(filename, 'wb') as f:
		pickle.dump(item, f)


def load_binary(filename):
	"""
	Parameters:
		filename: the specific binary file to load

	Return Value:
		whatever was stored in `filename`
	"""
	with open(filename, "rb") as f:
		return pickle.load(f, encoding='binary')


def main():
	_, val = get_corpus_metrics(DATA_DIR, True, 0.3)
	print(val)


if __name__ == '__main__':
	main()

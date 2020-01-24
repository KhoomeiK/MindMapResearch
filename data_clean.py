import os, csv
import nltk

DATA_DIR = 'data'
LABELS = ['sadder', 'bet_sad', 'neutral', 'bet_hap', 'happier']

def get_texts():
	happier, bet_hap, neutral, bet_sad, sadder = [], [], [], [], []
	for label in LABELS:
		directory = os.path.join(DATA_DIR, label)
		for filename in os.listdir(directory):
		    with open(os.path.join(directory, filename), encoding='utf-8') as f:
		    	data = csv.reader(f, delimiter=',')
		    	next(data)
		    	for row in data:
		    		pt = {"author":row[0], "self_id":row[1], "parent_id":row[2], "text":row[3]}
		    		if label == "sadder":
		    			sadder.append(pt)
		    		if label == "bet_sad":
		    			bet_sad.append(pt)
		    		if label == "neutral":
		    			neutral.append(pt)
		    		if label == "bet_hap":
		    			bet_hap.append(pt)
		    		if label == "happier":
		    			happier.append(pt)
	return happier, bet_hap, neutral, bet_sad, sadder
	

# this has to be done together because the set() operation has to be on all text	
def get_corpus_metrics(h, bh, n, bs, s, remove_punctuation=False):
	def metrics(text):
		return len(text), len(set(text))

	corpus = []
	for item in h:
		if item['text'] != '':
			corpus.extend(nltk.word_tokenize(item['text']))
	for item in s:
		if item['text'] != '':
			corpus.extend(nltk.word_tokenize(item['text']))
	for item in bh:
		if item['text'] != '':
			corpus.extend(nltk.word_tokenize(item['text']))
	for item in n:
		if item['text'] != '':
			corpus.extend(nltk.word_tokenize(item['text']))
	for item in bs:
		if item['text'] != '':
			corpus.extend(nltk.word_tokenize(item['text']))

	if remove_punctuation:
		corpus = [c for c in corpus]

	return metrics(corpus)


def main():
	h, bh, n, bs, s = get_texts()
	corpus_size, vocabulary_size = get_corpus_metrics(h, bh, n, bs, s, remove_punctuation=True)

	# With Punctuation
	#     4726685    , 112261
	print(corpus_size, vocabulary_size)


if __name__ == '__main__':
	main()
import torch, os
import numpy as np

from infersent.models import InferSent

import pickle
import time

MODEL_PATH = 'encoder/infersent2.pkl'
W2V_PATH = 'fastText/crawl-300d-2M.vec'
DATA_PATH = 'data-manipulation/data.pkl'

def load_infersent_model(model_path=MODEL_PATH, word_embeddings_path=W2V_PATH):
	params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048, 'pool_type': 'max', 'dpout_model': 0.0, 'version': 2}
	infersent = InferSent(params_model)
	infersent.load_state_dict(torch.load(model_path))
	infersent.set_w2v_path(word_embeddings_path)
	infersent.build_vocab_k_words(K=100000)
	return infersent

def get_infersent_vectors(sentences, model):
	return model.encode(sentences, tokenize=False, verbose=False)

def get_user_data_embeddings(comments, model):
	embedding = get_infersent_vectors(comments, model)
	return embedding

def get_current_embeddings(mypath):
	onlyfiles = [f[:-4] for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	return onlyfiles

dataEmbeddings = []
model = load_infersent_model()

print('data loading')
with open(DATA_PATH, 'rb') as f:
    names, data = pickle.load(f)
print('data loading done')

current = get_current_embeddings('embeddings')

for i, name in enumerate(names):
	comments = list(data[i]['text']) if 'text' in data[i] else []
	if len(comments) >= 1:
		if name in current:
			print('{} {}\'s embedding has already been generated'.format(i, name))
		else:
			try:
				embeddings = get_user_data_embeddings(data[i]['text'], model)
				print(len(embeddings), 'comments')
				dataEmbeddings.append(embeddings)
				print('Created embedding for {} ({}/{})'.format(name, i, len(names)))
				with open('embeddings/%s.pkl' % name, 'wb') as pkl:
					pickle.dump(embeddings, pkl)
			except:
				print('ERROR')

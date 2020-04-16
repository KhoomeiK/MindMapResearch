from os import listdir
from os.path import isfile, join
import pandas as pd
from filter import create_mappings
import pickle

mypath = 'users'
csvs = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(len(csvs))

# data = []
# names = []
# for csv in csvs:
# 	if csv[-4:] == '.csv':
# 		try:
# 			data.append(pd.read_csv(join(mypath, csv), encoding='CP1252'))
# 			names.append(csv[:-4])
# 		except:
# 			try:
# 				data.append(pd.read_csv(join(mypath, csv), encoding='UTF8'))
# 				names.append(csv[:-4])
# 			except:
# 				continue
# print(len(data))

### DO THIS IF YOU ARE USING A FRESH DATASET ###
# a = [names, data]

# with open('data.pickle', 'wb') as handle:
# 	pickle.dump(a, handle, protocol=3)

# with open('data.pickle', 'rb') as handle:
# 	b = pickle.load(handle)

# with open('data.pickle', 'rb') as handle:
#     names, data = pickle.load(handle)

# scores, nd = create_mappings(names, data)

# with open('labels.pickle', 'wb') as handle:
# 	pickle.dump(scores, handle, protocol=3)

with open('labels.pickle', 'rb') as handle:
	b = pickle.load(handle)

from pprint import PrettyPrinter as pp

p = pp(indent=4)
p.pprint(list(b.items())[:10])

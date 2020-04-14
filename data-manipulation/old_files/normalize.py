import pickle
import h5py
import numpy as np
import matplotlib.pyplot as plt
from pprint import PrettyPrinter as pp
from scipy.stats import boxcox


# 1) NON GAY DIST
# 2) 2std or 3std away from mean (cut em out)
# 3) HDF5


class Normalize:
	def __init__(self, filename):
		"""
		filename: the filename of the labels_dict
		labels_dict: the raw dictionary of the labels
		printer: pretty printer object for convenience
		depression_percentage: numpy array of depression percentages in order of labels_dict.keys()
		vader_score: numpy array of vader scores in order of labels_dict.keys()
		"""
		self.filename = filename
		with (open(filename, 'rb')) as f:
			self.labels_dict = pickle.load(f)
		self.printer = pp(indent=4)
		self.add_scores()
		self.vader_score = np.asarray(self.vader_score)
		self.depression_percentage = np.asarray(self.depression_percentage)

	def add_scores(self):
		"""
		helper function to add in individual arrays out of labels_dict
		"""
		self.depression_percentage = []
		self.vader_score = []
		for k in self.labels_dict.keys():
			self.depression_percentage.append(self.labels_dict[k][0])
			self.vader_score.append(self.labels_dict[k][1])
			# self.labels_dict[k] = np.asarray(self.labels_dict[k])

	def show_labels(self):
		"""
		print out the labels dict
		"""
		self.printer.pprint(self.labels_dict)

	def show_percentages(self):
		"""
		print out the depression percentages array
		"""
		self.printer.pprint(self.depression_percentage)

	def show_vader(self):
		"""
		print out the vader scores array
		"""
		self.printer.pprint(self.vader_score)

	def get_percentages(self):
		"""
		get the depression percentages array
		"""
		return self.depression_percentage

	def get_vader(self):
		"""
		get the vader scores array
		"""
		return self.vader_score

	def write(self, filename='labels.pkl'):
			"""
			update labels_dict pickle file to latest version in here
			"""
			if self.labels_dict is not None:
				with open(filename, 'wb') as f:
					pickle.dump(self.labels_dict, f)

	def get_hist(self, data, transform="", log=False, save=False):
		"""
		generate a histogram for a (n, 1) numpy array
		data: (n, 1) shaped numpy array to generate histogram for
		transform: the transformation you did to the data (to include in plot title)
		log: if set to True, x-axis is log-transformed
		save: if False, nothing, otherwise set this to the filename of the png you want the plot to save to
		"""
		plt.hist(data, bins='auto', log=log, color="#2980b9")
		plt.xlabel('independent variable')
		plt.ylabel('frequency')

		def metrics(d):
			return np.mean(d), np.std(d)
		mu, std = metrics(data)
		if transform == "":
			title = "Histogram for data with mu = %.6f,  std = %.6f" % (
				mu, std)
		else:
			title = "Transform " + transform + \
				" and mu = %.6f,  std = %.6f" % (mu, std)
		plt.title(title)
		# plt.title('Frequency of independent variable')
		if save:
			plt.savefig(save)
		plt.show()

	def update_labels(self, percentages, vader):
		"""
		update the labels_dict with a new set of depression percentages and vader scores
		percentages: an (n, 1) shape numpy array of depression percentages
		vader: an (n, 1) shape numpy array of vader scores
		"""
		for p, v, k in zip(percentages.tolist(), vader.tolist(), self.labels_dict.keys()):
			self.labels_dict[k][0] = p
			self.labels_dict[k][1] = v
		self.depression_percentage = percentages
		self.vader_score = vader


def main():
	norm = Normalize('labels.pkl')

	def softmax(x):
		return np.exp(x) / np.sum(np.exp(x), axis=0)

	p = pp(indent=4)
	p.pprint(norm.labels_dict[list(norm.labels_dict.keys())[0]])
	norm.write()

	# data_standard = norm.get_percentages()
	# norm.get_hist(data_standard, save='img/percentages_raw.png')

	# data = 650 * data_standard
	# norm.get_hist(data, transform='data * 650', save='img/percentages_scale.png')

	# data = np.where(650 * data_standard > 5, 5, 650 * data_standard)
	# norm.get_hist(data, transform='data > 5 = 5', save='img/percentages_map.png')

	# data = softmax(data_standard)
	# norm.get_hist(data, transform='softmax', save='img/percentages_softmax.png')

	# data = np.tanh(data_standard)
	# norm.get_hist(data, transform='tanh', save='img/percentages_tanh.png')

	# data = boxcox(.001 + 650 * data_standard, 0.0)
	# norm.get_hist(data, transform='boxcox: lambda = 0', save='img/percentages_log-transform.png')

	# data = boxcox(.001 + 650 * data_standard, 0.5)
	# norm.get_hist(data, transform='boxcox: lambda = 0.5', save='img/percentages_square-root-transform.png')

	# data_standard = norm.get_vader()
	# norm.get_hist(data_standard, save='img/vader_raw.png')

	# data = 650 * data_standard
	# norm.get_hist(data, transform='data * 650', save='img/vader_scale.png')

	# data = np.where(650 * data_standard > 5, 5, 650 * data_standard)
	# norm.get_hist(data, transform='data > 5 = 5', save='img/vader_map.png')

	# data = softmax(data_standard)
	# norm.get_hist(data, transform='softmax', save='img/vader_softmax.png')

	# data = np.tanh(data_standard)
	# norm.get_hist(data, transform='tanh', save='img/vader_tanh.png')

	# data = boxcox(.001 + 650 * np.absolute(data_standard), 0.0)
	# norm.get_hist(data, transform='boxcox: lambda = 0', save='img/vader_log-transform.png')

	# data = boxcox(.001 + 650 * np.absolute(data_standard), 0.5)
	# norm.get_hist(data, transform='boxcox: lambda = 0.5', save='img/vader_square-root-transform.png')


if __name__ == '__main__':
	main()

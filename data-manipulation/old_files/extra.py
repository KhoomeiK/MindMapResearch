def write(self, filename='labels.hdf5'):
		"""
		update labels_dict pickle file to latest version in here
		"""
		if self.labels_dict is not None:
			with open('labels.pickle', 'wb') as f:
				pickle.dump(self.labels_dict, f)
			# print("Saving labels dictionary to HDF5")
			# self.save_dict_to_hdf5(self.labels_dict, filename)


def save_dict_to_hdf5(self, dic, filename):
	"""
	....
	"""
	with h5py.File(filename, 'w') as h5file:
		self.recursively_save_dict_contents_to_group(h5file, '/', dic)


def recursively_save_dict_contents_to_group(self, h5file, path, dic):
	"""
	....
	"""
	for key, item in dic.items():
		if isinstance(item, (np.ndarray, np.int64, np.float64, str, bytes)):
			h5file[path + key] = item
		elif isinstance(item, dict):
			self.recursively_save_dict_contents_to_group(
				h5file, path + key + '/', item)
		else:
			raise ValueError('Cannot save %s type' % type(item))


def load_dict_from_hdf5(self, filename):
	"""
	....
	"""
	with h5py.File(filename, 'r') as h5file:
		return self.recursively_load_dict_contents_from_group(h5file, '/')


def recursively_load_dict_contents_from_group(self, h5file, path):
	"""
	....
	"""
	ans = {}
	for key, item in h5file[path].items():
		if isinstance(item, h5py._hl.dataset.Dataset):
			ans[key] = item.value
		elif isinstance(item, h5py._hl.group.Group):
			ans[key] = self.recursively_load_dict_contents_from_group(h5file, path + key + '/')
	return ans
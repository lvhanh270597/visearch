class Counter:
	"""docstring for Counter"""
	def __init__(self, data=None):
		if data is None:
			self.data = dict()
			self.whattype = None
		else:
			if type(data) == dict:
				self.data = data
				self.whattype = self.get_type_of_dict(data)
			elif type(data) == list:
				self.whattype = int
				self.data = dict.fromkeys(set(data), 0)
				for w in data: self.data[w] += 1
			else:
				data = list(data)
				self.whattype = int
				self.data = dict.fromkeys(set(data), 0)
				for w in data: self.data[w] += 1
	def get_type_of_dict(self, d):
		if len(d) == 0: return None
		for v in d:
			return type(d[v])
	def update(self, _dict):		
		for key in _dict.keys():
			if key in self.data:
				self.data[key] += _dict.get(key)
			else:
				self.data[key] = _dict.get(key)
	def get(self, key):		
		return self.data[key]
	def exist(self, key):
		return key in self.data
	def keys(self):
		return self.data.keys()
	def values(self):
		return self.data.values()
	def len(self):
		return len(self.data)
	def items(self):
		return self.data.items()
	def __str__(self):
		return 'Counter(%s)' % (str(self.data))	
		
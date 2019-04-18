from collections import Counter
from visearch.model.preprocessing import Preprocessor
class Querier:
	"""docstring for Query"""
	def __init__(self, correct_path, number_queries):
		self.preprocessor = Preprocessor(extract_entity=True, word_tokenize=True, correct_query=correct_path, num_query=3, lower_first=False)
		self.limit = number_queries
	def set_query(self, sentence):
		self.query = sentence
		queries = self.preprocessor.transform(sentence)
		if len(queries) > 0:
			non_tokenize = queries[0].replace('_', ' ')
			self.queries = queries[:1]
			self.queries.append(non_tokenize)
			self.queries.append(sentence)
			self.queries.extend(queries[1:])
		else:
			self.queries = [sentence]
		self.queries = self.queries[:self.limit]
		self.build_word_count()
	def build_word_count(self):
		self.word_counts = []
		for query in self.queries:
			self.word_counts.append(Counter(query.split()))
	def get_queries(self):
		return self.queries
	def get_max_prop_query(self):	
		return self.queries[0]
	def get_entities(self):
		return self.preprocessor.get_current_entities()
	def get_word_count(self):
		return self.word_counts
		'''
		([anh, yêu, em], [ảnh, yêu, em]) ==> {anh : 1, yêu: 1, em:1,  ảnh:1}
		'''
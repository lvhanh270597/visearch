from visearch.datastructures.counter import Counter
#from collections import Counter

class Indexer:
	"""docstring for Indexer"""
	def __init__(self, preprocessor):
		self.preprocessor = preprocessor
	def set_fields(self, fields):
		self.fields = [field for (field, stored) in fields.items() if stored]
		self.non_stored_fields = [field for (field, stored) in fields.items() if not stored]
		self.word_docs = []
		self.word_counts = []		
		self.ref_entities = Counter()
		self.more_info = []
		self.df = {field : Counter() for field in self.fields}
		self.ref_docs = {field : Counter() for field in self.fields}
		self.list_update = {field : set() for field in self.fields}		
		self.n_size = 0
	def get_updated_docs(self, field, list_words):
		for word in list_words:
			if self.ref_docs[field].exist(word):
				self.list_update[field].update(set(self.ref_docs[field].values()))
	def get_reference_entity_doc(self, entities):
		reference_docs = set()
		for entity in entities:
			if entity in self.ref_entities.keys():
				reference_docs.update(self.ref_entities.get(entity))
		res = dict.fromkeys(reference_docs, set(self.fields))
		return res
	def set_null_update(self):
		self.list_update = {field : set() for field in self.fields}
	def add_document(self, document, update=True):
		i = self.n_size
		word_counts = dict()
		word_doc = dict()
		entities_of_doc = set()
		for field in self.fields:
			word_counts[field] = self.transform(document[field])			
			word_doc[field] = tuple(document[field].split())
			
			if update: self.get_updated_docs(field, word_counts.keys())

			self.df[field].update(Counter(word_counts[field].keys()))
			self.ref_docs[field].update({key : [i] for key in word_counts[field].keys()})						
			entities_of_doc.update(self.preprocessor.get_current_entities())			
		self.word_counts.append(word_counts)
		self.word_docs.append(word_doc)		
		self.ref_entities.update(dict.fromkeys(entities_of_doc, [i]))
		self.more_info.append(tuple([document[field] for field in self.non_stored_fields]))
		self.n_size += 1			
	def fit(self, docs):			
		for i, document in enumerate(docs):
			print('Processing at %d/%d %.2f' %(i, len(docs), (i / len(docs)) * 100))
			self.add_document(document, update=False)
	def transform(self, sentence):		
		word_counts = Counter()
		for sentence in self.preprocessor.transform(sentence):			
			word_counts.update(Counter(sentence.split()))			
		return word_counts
		'''
		anh yêu em ==> {anh : 1, yêu: 1, em:1 }
		'''
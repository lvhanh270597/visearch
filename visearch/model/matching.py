from visearch.algorithm.matching import *
import time

class Matcher:
	"""docstring for Matcher"""
	def __init__(self, querier, indexer, vectorizer, max_result_per_query):		
		self.querier = querier
		self.indexer = indexer
		self.vectorizer = vectorizer		
		self.max_operate_ngram = 10000
		self.max_operate_med = 700
		self.min_similarity = 0
		self.max_result_per_query = max_result_per_query
	def set_raw_query(self, query):
		self.querier.set_query(query)		
	def get_reference_entities_docs(self):
		entities = self.querier.get_entities()
		self.reference_entities = self.indexer.get_reference_entity_doc(entities)
	def matching(self):
		self.total_reference_docs = set()
		start = time.time()
		word_counts = self.querier.get_word_count()
		queries = self.querier.get_queries()
		print('Section 1: %f' %(time.time() - start))
		start = time.time()
		self.get_reference_entities_docs()
		print('Section 2: %f' %(time.time() - start))	
		start = time.time()
		scores = []
		for query, word_count in zip(queries, word_counts):
			start_query = time.time()
			scores.append(self.matching_query(query, word_count))
			self.total_reference_docs.update(self.reference_docs)
			print('Section query %s: %f' %(query, time.time() - start_query))	
		print('Section 3: %f' %(time.time() - start))	
		start = time.time()
		total_score = dict.fromkeys(self.total_reference_docs, 0)		
		i = len(queries)
		for cur_scores in scores:
			for _id in cur_scores:
				total_score[_id] = max(total_score[_id], cur_scores[_id] * i)
			i -= 1
		self.result = [(_id, total_score[_id]) for _id in sorted(total_score, key=total_score.get, reverse=True)]
		print('Section 4: %f' %(time.time() - start))			
	def get_result(self):
		return self.result
	def matching_query(self, query, word_count):
		# get reference docs
		self.reference_docs = self.vectorizer.get_reference_docs(word_count.keys())				
		self.reference_docs.update(self.reference_entities)		
		res = []
		first = True
		while first or (len(self.reference_docs) > self.max_result_per_query):
			self.size_fields = {field : 0 for field in self.vectorizer.fields}
			for doc in self.reference_docs:
				for field in self.reference_docs[doc]:
					self.size_fields[field] += len(self.indexer.word_docs[doc][field])
			self.size_fields = dict([(k, self.size_fields[k]) for k in sorted(self.size_fields, key=self.size_fields.get)])
			print(self.size_fields)
			list_words = query.split()

			# get matching cosine		
			start = time.time()
			score1 = self.matching_consine(word_count)
			print(score1)
			print('cosine: %f' %(time.time() - start))
			# get matching n-grams		
			start = time.time()
			score2 = self.matching_ngram(list_words)
			print('n_gram_matching: %f' %(time.time() - start))	
			# get matching maximum_edit_distance
			start = time.time()
			score3 = self.matching_maximum_edit_distance(list_words)
			print('med_score: %f' %(time.time() - start))	
			# total score
			total = dict()
			for _id in self.reference_docs:			
				total[_id] = score1[_id] + score2[_id] + score3[_id]			
			res = [(k, total[k]) for k in sorted(total, key=total.get, reverse=True) if total[k] > self.min_similarity]
			reference_docs = [k for (k, v) in res]
			temp_ref = dict()
			n_size = len(reference_docs)
			if n_size > self.max_result_per_query:
				for doc in reference_docs[: n_size // 2]:
					temp_ref[doc] = self.reference_docs[doc]
				self.reference_docs = temp_ref
				res = dict(res[: n_size // 2])
			else:
				res = dict(res)
			first = False		
		return res
	def matching_consine(self, word_count):
		return self.vectorizer.get_similarity(word_count, self.reference_docs)
	def matching_ngram(self, list_words):
		# select fields
		fields, sum_operate, select_fields, i = list(self.vectorizer.fields), 0, [], 0
		while (sum_operate < self.max_operate_ngram) and (i < len(fields)):
			cur_field = fields[i]
			sum_operate += self.size_fields[cur_field]
			if sum_operate < self.max_operate_ngram:
				select_fields.append(cur_field)			
			i += 1
		# calculate
		n_gram_score = dict()
		for _id in self.reference_docs:
			n_gram_score[_id] = 0
			word_doc = self.indexer.word_docs[_id]
			for field in select_fields:
				n_gram_score[_id] += n_gram_matching(list_words, word_doc[field])		
		return n_gram_score
	def matching_maximum_edit_distance(self, list_words):
		# select fields
		fields, sum_operate, select_fields, i = list(self.vectorizer.fields), 0, [], 0
		while (sum_operate < self.max_operate_med) and (i < len(fields)):
			cur_field = fields[i]
			sum_operate += self.size_fields[cur_field]
			if sum_operate < self.max_operate_med:
				select_fields.append(cur_field)			
			i += 1
		# calculate
		med_score = dict()        
		for _id in self.reference_docs:
			med_score[_id] = 0
			word_doc = self.indexer.word_docs[_id]
			for field in select_fields:
				med_score[_id] += minimum_edit_distance(list_words, word_doc[field])            
		return med_score
		
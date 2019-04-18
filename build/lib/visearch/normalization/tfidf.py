from math import log2
from visearch.algorithm.matching import cosine

class tfIdf:
    def __init__(self, indexer, min_tfidf=0.05, max_tfidf=100):
        self.indexer = indexer
        self.vectors = []        
        self.tfidf = lambda tf, max_tf, doc_size, df: (tf / max_tf) * log2(doc_size / df)
        self.min_tfidf = min_tfidf
        self.max_tfidf = max_tfidf
        self.stopwords = dict()
    def set_fields(self, fields):        
        self.indexer.set_fields(fields)    
        self.fields = self.indexer.fields
    def fit(self, docs):
        self.indexer.fit(docs)
        self.doc_size = self.indexer.n_size
        if self.doc_size > 0: self.max_tfidf = log2(self.doc_size)
        #build list of vectors
        for i, word_counts in enumerate(self.indexer.word_counts):
            print('Build vector at %d/%d %.2f' %(i, self.doc_size, (i / self.doc_size) * 100))
            vector = self.build_vector(word_counts)
            self.vectors.append(vector)        
    def get_similarity(self, word_counts, list_indices):
        vector_sen = self.transform(word_counts)        
        sim = {field : dict() for field in self.fields}
        scores = dict()
        for _id in list_indices:
            scores[_id] = 0            
            vector_doc = self.vectors[_id]            
            for field in list_indices[_id]:
                score = cosine(vector_sen[field], vector_doc[field])
                sim[field][_id] = score
                scores[_id] += score
        return scores
    def get_reference_docs(self, list_words):        
        ref_docs = {field : set() for field in self.fields}                
        for word in list_words:
            for field in self.fields:                
                if self.indexer.ref_docs[field].exist(word):
                    ref_docs[field].update(self.indexer.ref_docs[field].get(word))
        res = dict()
        for field in self.fields:
            for doc in ref_docs[field]:
                if doc not in res: res[doc] = {field}
                else: res[doc].add(field)
        return res
    def build_vector(self, word_counts):
        vector = dict()
        for field in self.fields: 
            vector[field] = dict()     
            max_tf = max(list(word_counts[field].values()) + [0])
            for (word, count) in word_counts[field].items():
                if not self.indexer.df[field].exist(word):
                    value = 0 
                else:
                    value = self.tfidf(count, max_tf, self.doc_size, self.indexer.df[field].get(word))
                if (value < self.min_tfidf) or (value > self.max_tfidf):
                    self.stopwords[word] = value                    
                else:                    
                    vector[field][word] = value
        return vector
    def build_vector_query(self, word_count):
        vector = dict()
        max_tf = max(list(word_count.values()) + [0])
        for field in self.fields: 
            vector[field] = dict()
            for (word, count) in word_count.items():
                if self.indexer.df[field].exist(word):
                    vector[field][word] = \
                    self.tfidf(count, max_tf, self.doc_size, self.indexer.df[field].get(word))
        return vector
    def transform(self, word_count):
        vector = self.build_vector_query(word_count)        
        return vector
    def add_new_document(self, document):
        self.indexer.add_document(document)
        word_counts = self.indexer.word_counts[-1]
        vector = self.build_vector(word_counts)
        self.vectors.append(vector)

        list_update_docs = self.indexer.list_update
        self.indexer.set_null_update()
        for field in list_update_docs:
            for id_doc in list_update_docs[field]:
                self.update(id_doc, field)
    def update(self, id_doc, field):
        # this is because of affected document when add new
        vector_field = dict()
        for word, count in self.indexer.word_counts[id_doc][field]:
            if self.indexer.df[field].exist(word):
                vector_field[word] = \
                self.tfidf(count, max_tf, self.doc_size, self.indexer.df[field][word])
        self.vectors[id_doc][field] = vector_field
from visearch.model.preprocessing import Preprocessor
from visearch.model.indexing import Indexer
from visearch.model.querier import Querier
from visearch.normalization.tfidf import tfIdf
from visearch.model.matching import Matcher
from visearch.algorithm.matching import n_gram_matching, minimum_edit_distance

class Searcher:
    def __init__(self, correct_path, number_queries=3, number_results=10):
        self.indexer = Indexer(Preprocessor(extract_entity=True, word_tokenize=True))
        self.vectorizer = tfIdf(self.indexer)
        self.querier = Querier(correct_path, number_queries)
        self.matcher = Matcher(self.querier, self.indexer, self.vectorizer, number_results)        
    def set_fields(self, fields):
        self.fields = fields
        self.vectorizer.set_fields(fields)
    def fit(self, docs):                
        self.vectorizer.fit(docs)    
    def get_info_doc(self, list_ids):
        res = []
        for _id, score in list_ids:
            res.append((self.indexer.more_info[_id], score))
        return res
    def add_document(self, doc):
        self.vectorizer.add_new_document(doc)
    def search(self, query):
        self.matcher.set_raw_query(query)
        self.matcher.matching()
        self.scores = self.matcher.get_result()
        res = self.get_info_doc(self.scores)
        print(res)
        return {
            'results' : res,
            'queries' : self.querier.get_queries()
        }
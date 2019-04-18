import re, pickle
from pyvi import ViTokenizer
from visearch.datastructures.sentence import Sentence

class Preprocessor:
    def __init__(self, remove_stopword=False, correct_query=False, num_query=1, extract_entity=False, word_tokenize=False, lower_first=True):
        self.remove_stopword = remove_stopword
        self.correct_query = correct_query
        self.num_query = num_query
        self.extract_entity = extract_entity
        self.word_tokenize = word_tokenize
        self.lower_first = lower_first
        if self.extract_entity:
            self.entities = set()
        if self.remove_stopword:
            self.stopwords = set()
        self.load_data()
    def load_data(self):        
        if self.correct_query:
            self.correct = pickle.load(open(self.correct_query, 'rb'))
    def transform(self, sentence):
        sentence = Sentence(sentence, self.lower_first).get()
        sentences = [sentence]
        if self.correct_query:
            sentences = self.correct.predict([sentence])[0][:self.num_query]
        if self.extract_entity:
            self.cur_entities = set(Sentence(sentence).extract('name'))
            self.entities.update(self.cur_entities)
        if self.word_tokenize:
            for i, sentence in enumerate(sentences):
                sentences[i] = ViTokenizer.tokenize(sentence)
        if self.remove_stopword:            
            for i, sentence in enumerate(sentences):                
                sentences[i] = ' '.join([word for word in sentence.split()\
                                        if word not in self.stopwords])
        return sentences
    def get_current_entities(self):
        return self.cur_entities
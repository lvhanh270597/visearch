'''from preprocessing import Preprocessor

preprocessor = Preprocessor(word_tokenize=True, remove_stopword=False, extract_entity=True, num_query=2)

print(preprocessor.transform("Hom qua em den truong tai Ha Noi, me dat tay tung buoc den Sai Gon"))
print(preprocessor.entities)''' 
from os import listdir
from search import Searcher
searcher = Searcher()
fields = {
	'id' : False, 
	'title' : True,
	'content' : True,
	'out' : False
}

docs = []
for fname in listdir('./data/folders/1001 bí ẩn/'):	
	item = {
		'id' : len(docs) + 1,
		'title' : fname[:-4],
		'content' : open('./data/folders/1001 bí ẩn/' + fname).read(),
		'out' : fname[:-4]
	}
	docs.append(item)

searcher.set_fields(fields)
searcher.fit(docs[:10])
for i in range(10):
	print(docs[i]['title'])
i = 10
while True:		
	s = input('Already to test: ')	
	if s == 'add':
		print(docs[i]['title'])
		searcher.add_document(docs[i])
		i += 1
	else: searcher.search(s)	
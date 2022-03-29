from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors

"""
model_shiroyagi_path = '/Users/yamashitashiori/Desktop/Python3/latest-ja-word2vec-gensim-model/word2vec.gensim.model'
model_shiroyagi = Word2Vec.load(model_shiroyagi_path)
print(model_shiroyagi.wv.similarity("笑う", "笑い"))
results = model_shiroyagi.most_similar(positive=['笑う'])
for result in results:
    print(result)

from gensim.models import KeyedVectors
model_okazaki_dir = '/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/entity_vector/entity_vector.model.bin'
model_okazaki = KeyedVectors.load_word2vec_format(model_okazaki_dir, binary=True)

results = model_okazaki.most_similar(u'[笑い]')
for result in results:
    print(result)


model_path = '/Users/yamashitashiori/Desktop/Python3/ja/ja.bin'
model = Word2Vec.load(model_path)
print(model.wv.similarity("日本", "ドイツ"))
results = model.most_similar(positive=['空き缶'])
for result in results:
    print(result)

"""

model_dir = '/Users/yamashitashiori/Desktop/Python3/chive-1.1-mc90-aunit_gensim/chive-1.1-mc90-aunit.kv'
model = KeyedVectors.load(model_dir)

print(model.similarity("笑う", "泣く"))
results = model.most_similar(positive=['あたし'])
for result in results:
    print(result)
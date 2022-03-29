# 学習済みwoed2vecで遊んでみますわよ
import collections
import numpy as np
import pandas as pd
import sys
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import japanize_matplotlib
import string
from gensim.models.word2vec import Word2Vec

from gensim.models import KeyedVectors
model_dir = '/Users/yamashitashiori/Desktop/Python3/chive-1.1-mc90-aunit_gensim/chive-1.1-mc90-aunit.kv'
model = KeyedVectors.load(model_dir)
model_shiroyagi_path = '/Users/yamashitashiori/Desktop/Python3/latest-ja-word2vec-gensim-model/word2vec.gensim.model'
model_shiroyagi = Word2Vec.load(model_shiroyagi_path)

"""
results = model.most_similar(u'[吐く]')
for result in results:
    print(result)



('ときめき', 0.7825179100036621)
('れもん', 0.7589542865753174)
('さくら', 0.7530252933502197)
('やすらぎ', 0.7524086833000183)
('原宿', 0.7494283318519592)
('日和', 0.748458981513977)
('きらら', 0.7475771903991699)
('パオパオ', 0.74507075548172)
('キラリ', 0.7401843070983887)
('ふれあい', 0.7380743026733398)

"""

#これで単語のベクトル表示ができるようになったから、次は米津玄師の歌詞中に出てくる単語をネットワークみたいな感じで可視化したい！
"""
歌詞に含まれる単語ごとのネットワーク分析
行と列を各単語にして、その成分として類似度を入れる
各ノード（単語）の大きさはその単語の出現回数に依存させる
"""

stop_words = ['そう', 'ない', 'いる', 'する', 'まま', 'よう',
              'てる', 'なる', 'こと', 'もう', 'いい', 'ある',
              'ゆく', 'れる', 'なっ', 'ちゃっ', 'ちょっ',
              'ちょっ', 'やっ', 'あっ', 'ちゃう', 'その', 'あの',
              'この', 'どの', 'それ', 'あれ', 'これ', 'どれ',
              'から', 'なら', 'だけ', 'じゃあ', 'られ', 'たら', 'のに',
              'って', 'られ', 'ずっ', 'じゃ', 'ちゃ', 'くれ', 'なんて', 'だろ',
              'でしょ', 'せる', 'なれ', 'どう', 'たい', 'けど', 'でも', 'って',
              'まで', 'なく', 'もの', 'ここ', 'どこ', 'そこ', 'さえ', 'なく',
              'たり', 'なり', 'だっ', 'まで', 'ため', 'ながら', 'より', 'られる', 'です',"何","思う","の","さ","ん"]

#全曲の単語を結合する。
df = pd.read_csv("/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/lyric_kenshiyonezu_for_analyze.csv")
words_all = ' '.join(df['words'].tolist())
words_all_list = words_all.split(' ') #これだと、曲ごとには単語の重複はないが、曲をまたぐと単語の重複がある状態。ここから重複なく単語を取り出す。
words_kinds = list(set(words_all_list)) #これで一回ごとになった
words_for_model = []
#単語ごとの回数を数える
freq = collections.Counter(words_all_list)
words_freq_list = []

for word in words_kinds:
    if (freq[word] >= 5) and (word not in stop_words):
        if (word in model.index2word):
            words_for_model.append(word)
            words_freq_list.append(freq[word])
        elif word in model_shiroyagi.wv.index2word:
            words_for_model.append(word)
            words_freq_list.append(freq[word])

print(len(words_freq_list))

#各単語の類似度を算出して行列を作る
n = len(words_for_model)
matrix_similarity = np.zeros((n,n))

print(matrix_similarity.shape)

"""
for i in range(n):
    for j in range(n):
        similarity = model.wv.similarity(words_shiroyagi[i], words_shiroyagi[j])
        matrix_similarity[i][j] = similarity

print(matrix_similarity[0][1])
print(matrix_similarity.shape)
"""
"""
#ついに可視化
# グラフの生成
G = nx.Graph()
weight_list = []
for node in words_for_model:
    G.add_node(node)
for i in range(n-1):
    for j in range(i+1,n):
        #similarity = model.wv.similarity(words_for_model[i], words_for_model[j])
        if (words_for_model[i] in model.index2word) and (words_for_model[j] in model.index2word):
            similarity = model.similarity(words_for_model[i], words_for_model[j])
        elif (words_for_model[i] in model_shiroyagi.wv.index2word) and (words_for_model[j] in model_shiroyagi.wv.index2word):
            similarity = model_shiroyagi.wv.similarity(words_for_model[i], words_for_model[j])-0.15
        else:
            similarity = 0
        if similarity >= 0.6:
            G.add_edge(words_for_model[i], words_for_model[j],weight=similarity*0.0001)
            weight_list.append(similarity)

nx.draw_networkx(
    G,
    node_shape="s",
    node_size=np.array(words_freq_list)*5,
    width = ((np.array(weight_list)-0.6)/np.sum(np.exp(np.array(weight_list))))*1200,
    font_family ="IPAexGothic",
    font_size=5
)
plt.show()
"""

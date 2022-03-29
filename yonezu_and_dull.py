import numpy as np
import pandas as pd
from yonezu_kyouki_net import kyouki_matrix2,words_for_model,node_induces,nodes
#coding: UTF-8

df = pd.read_csv("/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/lyric_kenshiyonezu_for_analyze.csv")

"""
# 「笑う」「疲れる」「叫ぶ」「震える」「泣く」「怖い」「悲しい」「くだらない」「馬鹿」が含まれてる楽曲を抜き出す
laugh = []
get_tired = []
scream = []
shiver = []
cry = []
scared = []
sad = []
dull = []
stupid = []

for i in range(len(df)):
    if "笑う" in df.loc[i,'words']:
        laugh.append(df.loc[i,'曲名'])
    if "疲れる" in df.loc[i,'words']:
        get_tired.append(df.loc[i,'曲名'])
    if "叫ぶ" in df.loc[i,'words']:
        scream.append(df.loc[i,'曲名'])
    if "震える" in df.loc[i,'words']:
        shiver.append(df.loc[i,'曲名'])
    if "泣く" in df.loc[i,'words']:
        cry.append(df.loc[i,'曲名'])
    if "怖い" in df.loc[i,'words']:
        scared.append(df.loc[i,'曲名'])
    if "悲しい" in df.loc[i,'words']:
        sad.append(df.loc[i,'曲名'])
    if "くだらない" in df.loc[i,'words']:
        dull.append(df.loc[i,'曲名'])
    if "馬鹿" in df.loc[i,'words']:
        stupid.append(df.loc[i,'曲名'])



print("笑う:",laugh)
print("疲れる:",get_tired)
print("叫ぶ:",scream)
print("震える:",shiver)
print("泣く:",cry)
print("怖い:",scared)
print("悲しい:",sad)


print("くだらない:",dull)
print("馬鹿:",stupid)



# 「くだらない」「馬鹿」と共起してる単語を探してくる
# 「くだらない」「馬鹿」のwords_for_model内のインデックスを取得
dull_index = words_for_model.index("くだらない")
stupid_index = words_for_model.index("馬鹿")

# kyouki_matrixで、この2単語と多く共起してる単語のwords_for_modelでのインデックスを取得
dull_array_index2 = np.argsort(-kyouki_matrix2[dull_index])
dull_array_freq2 = np.sort(kyouki_matrix2[dull_index])[::-1]
stupid_array_index2 = np.argsort(-kyouki_matrix2[stupid_index])
stupid_array_freq2 = np.sort(kyouki_matrix2[stupid_index])[::-1]

dull_array_word = list(map(lambda i:words_for_model[i], dull_array_index2))
stupid_array_word = list(map(lambda i:words_for_model[i],stupid_array_index2))
print(dull_array_word)
print(stupid_array_word)
print(nodes)



print(dull_array_index2[0])
print(words_for_model.index("く"))
print(words_for_model.index("ら"))
print(dull_array_index2[0] in node_induces)


dull_array = []
stupid_array = []

j1 = 0
for i in range(100):
    if j1 == 10:
        break

    if dull_array_word[i] in nodes:
        dull_array.append(dull_array_word[i])
        j1 += 1
        print(j1)
    else:
        print(dull_array_word[i])

j2 = 0
for j in range(100):
    if j2 == 10:
        break

    if stupid_array_word[j] in nodes:
        stupid_array.append(stupid_array_word[j])
        j2 += 1
        print(j2)
    else:
        print(stupid_array_word[j])

# インデックスを単語に変換して出力
print(dull_array)
print(stupid_array)


"""
dull_index = words_for_model.index("くだらない")
stupid_index = words_for_model.index("馬鹿")
end_index = words_for_model.index("終わる")
chest_index = words_for_model.index("窓")

print(kyouki_matrix2[end_index,dull_index])
print(kyouki_matrix2[chest_index,dull_index])

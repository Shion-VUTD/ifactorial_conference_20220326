from word2vec_similaritynet import words_for_model,df,n,words_freq_list
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 主要358単語について共起ネットワークを作っていく

G = nx.Graph()
weight_list = []
kyouki_matrix = np.zeros((n,n))
kyouki_matrix2 = np.zeros((n,n))
for i in range(n-1):
    for j in range(i+1,n):
        kyouki_freq = 0
        for k in range(len(df)):
            if (words_for_model[i] in df.loc[k,"words"]) and (words_for_model[j] in df.loc[k,"words"]):
                kyouki_freq += 1

        kyouki_matrix2[i,j] = kyouki_freq
        kyouki_matrix2[j,i] = kyouki_freq

        if kyouki_freq >= 10:
            kyouki_matrix[i,j] = 1
            kyouki_matrix[j,i] = 1
            
kyouki_per_words = np.sum(kyouki_matrix,axis = 0)


nodes = []
node_induces = []
for i in range(len(words_for_model)):
    if (kyouki_per_words[i] <= 20) and (words_for_model[i] not in ['く','ら',' ','いく','一']):
        nodes.append(words_for_model[i])
        node_induces.append(i)
print(len(nodes))

"""
for node in nodes:
    G.add_node(node)
for i in range(len(nodes)-1):
    for j in range(i+1,len(nodes)):
        kyouki_freq = kyouki_matrix2[node_induces[i],node_induces[j]]
        if kyouki_freq >= 5:
            G.add_edge(nodes[i], nodes[j],weight=kyouki_freq*0.00000001)
            weight_list.append(kyouki_freq)
        


nx.draw_networkx(
    G,
    node_shape="s",
    node_size=8,
    width = ((np.array(weight_list)/np.sum(np.array(weight_list))))*18,
    font_family ="IPAexGothic",
    font_size=5,
    node_color="r"
)
plt.show()

"""
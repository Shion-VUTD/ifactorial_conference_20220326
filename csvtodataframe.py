import pandas as pd #pandasをpdとしてインポート
import MeCab
import numpy as np
from wordcloud import WordCloud
#%matplotlib inline
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/lyric_all.csv")

#データを整形したいですわよ
"""
1. 閲覧数をintにしたいですわよ
2. indexを保持したまま、歌詞を.txtに分離した方がいいかもですわよ
3. 形態素解析とかして、品詞や主要語のカラムを作りたいですわよ
"""


# intに書き換えるですわよ
displayed = df["表示回数"].to_numpy()

#displayed_frequency_int = []
#for frequency in displayed:
    #frequency = int(frequency.replace(",",""))
    #displayed_frequency_int.append(frequency)

#df["表示回数"] = displayed_frequency_int
#print(df.head(5))

# mecabで形態素解析する
aine_lyric = df.loc[0,"歌詞"]
#print(aine_lyric)
mecab = MeCab.Tagger("-Ochasen")
node = mecab.parseToNode(aine_lyric)
#print(node)

hcount = {}
while node:
    hinshi = node.feature.split(",")[0]
    if hinshi in hcount.keys():
        freq = hcount[hinshi]
        hcount[hinshi] = freq + 1
    else:
        hcount[hinshi] = 1
    node = node.next

#print(hcount)

def get_hinshifrequency(seq):
    text = str(seq).lower()
    node = mecab.parseToNode(text)
    hcount = {'名詞':0,"動詞":0,'連体詞':0,'副詞':0,"接頭詞":0,"形容詞":0,"接続詞":0}
    while node:
        hinshi = node.feature.split(",")[0]
        if hinshi in hcount.keys():
            freq = hcount[hinshi]
            hcount[hinshi] = freq + 1
        
        node = node.next

    return hcount

lyrics = df["歌詞"].to_numpy()

meishi = []
doushi = []
renntaishi =[]
fukushi = []
settoushi = []
keiyoushi = []
setsuzokushi = []

for lyric in lyrics:
    hinshifrequency_dict = get_hinshifrequency(lyric)
    meishi.append(hinshifrequency_dict['名詞'])
    doushi.append(hinshifrequency_dict['動詞'])
    renntaishi.append(hinshifrequency_dict['連体詞'])
    fukushi.append(hinshifrequency_dict['副詞'])
    settoushi.append(hinshifrequency_dict['接頭詞'])
    keiyoushi.append(hinshifrequency_dict['形容詞'])
    setsuzokushi.append(hinshifrequency_dict['接続詞'])

#print(meishi)

df['名詞'] = np.array(meishi)
df['動詞'] = np.array(doushi)
df['連体詞'] = np.array(renntaishi)
df['副詞'] = np.array(fukushi)
df['接頭詞'] = np.array(settoushi)
df['形容詞'] = np.array(keiyoushi)
df['接続詞'] = np.array(setsuzokushi)

#print(df.head(5))


#主要語のカラムを作るですわよ
#まずどんな単語が多いのか調べるですわよ

def text_to_words(text):
    
    words_song = []
    #分解した単語ごとにループする。
    seq = str(text).lower()
    node = mecab.parseToNode(seq)
    while node:
        word_type = node.feature.split(",")[0]
        #名詞、形容詞、副詞、動詞の場合のみ追加
        if word_type in ["名詞", "形容詞", "副詞", "動詞"]:
            word = node.feature.split(",")[6]           
            if word == "吐き出す":
                print(word)
                word2 = "吐く"
            else:
                word2 = word
            words_song.append(word2)            
        node = node.next
        
    #曲毎の単語の重複を削除して'空白区切のテキストを返す。
    words = ' '.join(set(words_song))
    return words

df["words"] = df["歌詞"].apply(text_to_words)

# wordcloud用の無意味そうな単語除去
stop_words = ['そう', 'ない', 'いる', 'する', 'まま', 'よう',
              'てる', 'なる', 'こと', 'もう', 'いい', 'ある',
              'ゆく', 'れる', 'なっ', 'ちゃっ', 'ちょっ',
              'ちょっ', 'やっ', 'あっ', 'ちゃう', 'その', 'あの',
              'この', 'どの', 'それ', 'あれ', 'これ', 'どれ',
              'から', 'なら', 'だけ', 'じゃあ', 'られ', 'たら', 'のに',
              'って', 'られ', 'ずっ', 'じゃ', 'ちゃ', 'くれ', 'なんて', 'だろ',
              'でしょ', 'せる', 'なれ', 'どう', 'たい', 'けど', 'でも', 'って',
              'まで', 'なく', 'もの', 'ここ', 'どこ', 'そこ', 'さえ', 'なく',
              'たり', 'なり', 'だっ', 'まで', 'ため', 'ながら', 'より', 'られる', 'です']

#全曲の単語を結合する。
words_all = ' '.join(df['words'].tolist())


#wordCloud生成
wordcloud = WordCloud(background_color="white",
                      font_path="/Library/Fonts/NotoSansCJKjp-Bold.otf", 
                      width=800, 
                      height=600,
                      collocations=False,
                      stopwords=set(stop_words),
                      regexp=r"\w[\w']+|[^ぁ-んァ-ン０-９a-zA-Z0-9\-!#$%&'()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]").generate(words_all)
#可視化
fig,ax = plt.subplots(figsize=(15,12))
ax.imshow(wordcloud)
ax.axis("off")

#保存
wordcloud.to_file("wordcloud_all3.png")

"""
#「吐く」？
haku_music = []
for i in range(len(lyrics)):
    if "吐き" in lyrics[i]:
        haku_music.append(df.loc[i,"曲名"]) 

print(haku_music) 
['caribou', 'クランベリーとパンケーキ', 'しとど晴天大迷惑', '鳥にでもなりたい', 'Neighbourhood', 'ひまわり', 'vivi', '笛吹けども踊らず', 'Flamingo', '街', 'ゆめくいしょうじょ']

sekai_music = []
for i in range(len(lyrics)):
    if "世界" in lyrics[i]:
        sekai_music.append(df.loc[i,"曲名"]) 

#print(sekai_music) 
#'あたしはゆうれい', 'ウィルオウィスプ', 'クランベリーとパンケーキ', '再上映', '春雷', 'シンデレラグレイ', 'でしょましょ', 'Nighthawks', 'Flowerwall', 'フローライト', 'ペトリコール', 'Paper Flower', 'ホープランド', 'ミラージュソング', 'メランコリーキッチン', 'リビングデッド・ユース'

douka_music = []
for i in range(len(lyrics)):
    if "どうか" in lyrics[i]:
        douka_music.append(df.loc[i,"曲名"]) 

#print(douka_music) 
#['amen', 'orion', '春雷', '砂の惑星 ( + 初音ミク)', 'Neon Sign', 'POP SONG', 'Lemon']

#原形に直して統計を取らないとダメっぽい
#print(df["words"].head(5))
#「吐く」「吐き出す」などの表記揺れがめんどくさい

#df.to_csv("/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/lyric_kenshiyonezu_for_analyze.csv",mode="w",encoding="utf-8",index=False)

"""
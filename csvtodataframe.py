import pandas as pd #pandasをpdとしてインポート
 
df = pd.read_csv("/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/lyric_test.csv")
print(df.head(5))

#データを整形したいですわよ
"""
1. 閲覧数をintにしたいですわよ
2. indexを保持したまま、歌詞を.txtに分離した方がいいかもですわよ
3. 形態素解析とかして、品詞や主要語のカラムを作りたいですわよ
"""
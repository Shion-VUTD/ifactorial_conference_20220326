import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


#webサイトを取得し、テキスト形式で出力
def load(url):
    res = requests.get(url)
    #HTTPリクエストが失敗したステータスコードを返した場合、HTTPErrorを送出
    res.raise_for_status()
    #レスポンスボディをテキスト形式で入手
    return res.text

#htmlタグの取得
def get_tag(html, find_tag):
    soup = BeautifulSoup(str(html), 'html.parser')
    tag = soup.find(find_tag)
    return tag

#htmlタグの取得
def get_tags(html, find_tag):
    soup = BeautifulSoup(str(html), 'html.parser')
    tag = soup.find_all(find_tag)
    return tag

#htmlのid取得
def get_id(html, find_id):
    soup = BeautifulSoup(str(html), 'html.parser')
    html_id = soup.select(find_id)
    return html_id

#プログラムで扱えるデータ構造に変換
def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    #htmlタグの削除
    simple_row = soup.getText()
    simple_row = simple_row.replace('　', '')    
    return simple_row

def parse_lyric(html):
    soup = BeautifulSoup(html, 'html.parser')
    #htmlタグの削除
    simple_row = soup.get_text(separator=" ").strip()
    simple_row = simple_row.replace('　', ' ')

    return simple_row

#それぞれ歌の情報の取得
def get_info(url):
    base_url = 'https://www.uta-net.com/'
    html = load(url)
    #曲ごとのurlを格納
    song_url = []
    #歌を格納
    song_info = []
    songs_info=[]

    #曲のurlを取得
    #tdのurlを格納
    for td in get_tags(html, 'td'):
        #a要素の取得
        for a in get_tags(td, 'a'):
            #href属性にsongを含むか否か
            if 'song' in a.get ('href'):
                #urlを配列に追加
                song_url.append(base_url + a.get('href'))

    #曲の情報の取得
    for i, page in enumerate(song_url):
        print('{}曲目:{}'.format(i + 1, page))
        html = load(page)
        song_info = []

        #Song
        for tag in get_tag(html, 'h2'):
            #id検索を行うため、一度strにキャスト
            tag = str(tag)
            simple_row = parse(tag)
            simple_row = simple_row.replace('\n','')
            song_info.append(simple_row)                

        #Artist
        for tag in get_tags(html, 'h3'):
            tag = str(tag)
            if r'itemprop="byArtist name"' in tag:
                simple_row = parse(tag)
                simple_row = simple_row.replace('\n','')
                song_info.append(simple_row)

        #Lyricist
        for tag in get_tags(html, 'a'):
            tag = str(tag)
            if r'itemprop="lyricist"' in tag:
                simple_row = parse(tag)
                song_info.append(simple_row)

        #Composer
        for tag in get_tags(html, 'a'):
            tag = str(tag)
            if r'itemprop="composer"' in tag:
                simple_row = parse(tag)
                song_info.append(simple_row)

        # 発売日、表示回数を取得
        for tag in get_tags(html, 'p'):
            tag = str(tag)
            if r'発売日'in tag:
                simple_row = parse(tag)
                simple_row = simple_row.replace(' ','')
                simple_row_list = simple_row.split('\n')
                dateimpression_seq = simple_row_list[3]
                dateimpression_seq = dateimpression_seq.replace("発売日：","")
                dateimpression_seq = dateimpression_seq.replace("回","")
                dateimpression_seq = dateimpression_seq.replace(",","")
                dateimpression_seq = dateimpression_seq.replace("この曲の表示数："," ")
                dateimpression_list = dateimpression_seq.split(' ')

                #発売日の取得
                song_info.append(dateimpression_list[0])
                #表示回数の取得
                song_info.append(int(dateimpression_list[1]))
       

        time.sleep(2)

        #Lyric
        for id_ in get_id(html, '#kashi_area'):
            id_ = str(id_)
            if r'id="kashi_area"' in id_:
                simple_row = parse_lyric(id_)
                song_info.append(simple_row)
                songs_info.append(song_info)

                #1秒待機(サーバの負荷を軽減)
                time.sleep(1)
                break



    return songs_info

def create_df(url):
    # データフレームを作成
    #df = pd.DataFrame('Song_Title', 'Artist', 'Lyricist', 'Composer', 'Lyric')
    df = pd.DataFrame(get_info(url))
    df = df.rename(columns={0:'曲名', 1:'歌手名', 2:'作詞者', 3:'作曲者', 4:'発売日',5:'表示回数',6:'歌詞'})
    return df
    

df = pd.DataFrame(columns={0:'曲名', 1:'歌手名', 2:'作詞者', 3:'作曲者', 4:'発売日',5:'表示回数',6:'歌詞'})
artist_num= 0
for artist_index in range(513,600):
    artist_num += 1
    url = 'https://www.uta-net.com/artist/'+str(artist_index)+'/'
    df_per_artist = create_df(url)

    #CSVファイル出力
    if artist_num==1:
        df_per_artist.to_csv('/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/lyric_all.csv', mode='a',header=False,encoding='utf-8',index=False)
    else:
        df_per_artist.to_csv('/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/lyric_all.csv', mode='a', header=False,encoding='utf-8',index=False)
   
    print(str(artist_num)+'番目のアーティストの情報をロードしました')
    



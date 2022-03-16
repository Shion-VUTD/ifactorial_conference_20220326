import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime

#スクレイピングしたデータを入れる表を作成
list_df = pd.DataFrame(columns=['曲名', '歌手名', '作詞者名', '作曲者名', '発売日', '表示回数', '歌詞'])
i = 0

for artist_index in range(1,31971):
    for page in range(1,2): #各アーティストから1ページずつとってくる
        base_url = 'https://www.uta-net.com'

        #歌詞一覧ページ
        url = 'https://www.uta-net.com/artist/'+str(artist_index)+'/0/' + str(page) + '/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('td', class_='side td1')

        for link in links:
            a = base_url + (link.a.get('href'))

            #歌詞詳細ページ
            response = requests.get(a)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 曲名を取得
            song_name = soup.find('h2').text

            # 歌手名を取得
            song_singer = soup.find('h3').text

            # 作詞者名を取得
            song_lyricwriter = soup.find('h4').text

            # 作曲者名を取得
            song_musicwriter = soup.find('th5').text

            # 発売日、表示回数などを取得
            detail = soup.find('p', class_="detail").text

            # 発売日を取得
            match = re.search(r'\d{4}/\d{2}/\d{2}', detail)
            release_date = datetime.strptime(match.group(), '%Y/%m/%d').date()

            # 表示回数を取得
            p = r'この曲の表示回数：(.*)回'
            impressions = re.search(p, detail).group(1)

            # 歌詞を取得
            song_lyrics = soup.find('div', itemprop='lyrics')
            song_lyric = song_lyrics.text
            song_lyric = song_lyric.replace('\n','')
            song_lyric = song_lyric.replace('この歌詞をマイ歌ネットに登録 >このアーティストをマイ歌ネットに登録 >','')
            

            #サーバーに負荷を与えないため1秒待機
            time.sleep(1)
            print('ロードを終了しました'+str(i)+'!')
            i += 1

            #取得した歌詞を表に追加
            tmp_se = pd.DataFrame([[song_name], [song_singer], [song_lyricwriter], [song_musicwriter], [release_date], [impressions], [song_lyric]], index=list_df.columns).T
            list_df = list_df.append(tmp_se,ignore_index=True)
            print(list_df)
            
        print('ページを更新しました')

    print('アーティストを更新しました')

#csv保存
list_df.to_csv('/Users/yamashitashiori/Desktop/Python3/ifactorial_conference_20220326/lyric_utanet_all.csv', mode = 'w', encoding='utf-8',index=False)
print("スクレイピングが終了しました")
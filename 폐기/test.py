import requests
from bs4 import BeautifulSoup
import json

def melon_search(search_word):
    
    url = 'https://www.melon.com/search/keyword/index.json'
    
    params = {
        'jscallback': 'jQuery19105357803934720518_1603168193882',
        'query': search_word
    }
    
    headers = {
        'Referer': 'https://www.melon.com/index.htm',
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                       (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36')
    }
    
    response = requests.get(url, headers = headers, params = params).text
    json_string = response.replace(params['jscallback'] + '(', '').replace(');', '')
    result_dict = json.loads(json_string)
    
    if len(result_dict['SONGCONTENTS']) == 0:
            print('멜론 검색 결과가 없습니다.')
    
    else:    
        print('\n멜론 "{}" 검색 결과(앨범명, 곡명, 곡정보 URL, 가사)\n'.format(result_dict['KEYWORD']))
        
        for song in result_dict['SONGCONTENTS']:
            print('''{ALBUMNAME} : {SONGNAME} : {ARTISTNAME}
https://www.melon.com/song/detail.htm?songId={SONGID}\n'''.format(**song))
           
            detail_url = 'https://www.melon.com/song/detail.htm?songId=' + song['SONGID']
            res_html = requests.get(detail_url, headers = headers).text
            
            soup = BeautifulSoup(res_html, 'html.parser')
            tag = soup.find(id='d_video_summary') # 가사
            tag = str(tag)
            tag = tag.replace('<div class="lyric" id="d_video_summary">', '').\
                replace('<!-- height:auto; 로 변경시, 확장됨 -->', '').\
                replace('<br/>', '/').replace('</div>', '').strip()
            tag = tag.replace('/', '\n')
            print(tag)
            
            print()


if __name__ == '__main__':
    line = input('검색어를 입력하시오> ')
    melon_search(line)
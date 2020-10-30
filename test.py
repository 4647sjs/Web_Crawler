#-*-coding:utf-8-sig-*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8-sig')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8-sig')
import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import csv
import re
import urllib
from urllib.request import HTTPError


"""
네이버 웹사이트 특정 단어 크롤러
"""

"""
TARGET_URL_BEFORE_KEWORD = 'https://search.naver.com/search.naver?f=&fd=2&filetype=0&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&query='
TARGET_URL_PAGE = '&research_url=&sm=tab_nmr&start='
TARGET_URL_REST = '&where=webkr'
"""


TARGET_URL_BEFORE_DATE = 'https://search.naver.com/search.naver?display=10&f=&filetype=0&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom'
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_PAGE = '&research_url=&sm=tab_nmr&start='
TARGET_URL_REST = '&where=web'

result=[]

headers = {"User Agent":"Mozilla/5.0"}


def get_link_from_news_title(URL, output_file):
    for i in range(81):
        if i%10==1:#네이버 페이지마다 10씩늘어나기 때문 최대 10페이지 제공
            URL_with_page_num = URL + str(i) + TARGET_URL_REST #URL 합치기
            URL_with_page_num = str(URL_with_page_num)
            print(URL_with_page_num)
            req = urllib.request.Request(URL_with_page_num, headers = headers)
            source_code_from_URL = urllib.request.urlopen(req)
            soup = BeautifulSoup(source_code_from_URL, 'lxml',from_encoding='utf-8')
            for item in soup.select('ul > li > div'): #포털 사이트 구조 분석 파악한 후 각 사이트의 URL 과 제목추출
                for item_link in item.select('div.total_tit > a'):
                    article_URL = item_link["href"] # URL 추출
                article_Title = item_link.text # 제목 추출
                get_text(article_URL, article_Title, output_file)


def remove_tag(content): # 데이터 가공 함수 미완성
    cleanr =re.compile(r'<(?!br).*?>') #tag 제거
    re_script = re.compile('<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.S | re.I) # script 제거
    css_script = re.compile('<\s*style[^>]*>.*?<\s*/\s*style\s*>', re.S | re.I) #css 제거
    cleanscript = re.sub(re_script, '', content)
    cleancss = re.sub(css_script, '', cleanscript)
    cleantext = re.sub(cleanr, '', cleancss)
    cleantext = re.sub(r'[\ \n]{2,}', '', cleantext)#일부 공백 제거
    cleantext = re.sub('\t*', '', cleantext)#일부 공백 제거
    return cleantext



def get_text(article_URL, article_Title, output_file): # 각 사이트의 body부분을 가져오는 함수
    print(article_URL)
    print(article_Title)
    try:
        req2 = urllib.request.Request(article_URL, headers=headers)
        #req2 = urllib.request.Request(article_URL)
        source_code_from_url = urllib.request.urlopen(req2)
    except HTTPError as e :
        print(e)
    except URLError as e:
        print('URL Not found')
    else:
        soup = BeautifulSoup(source_code_from_url, 'html.parser', from_encoding='utf-8-sig')
        content_of_article = str(soup.select('body'))  # body부분
        string_item = remove_tag(content_of_article)
        string_item = str(string_item)
        SaveToCSV(article_URL, article_Title, string_item, output_file)

def SaveToCSV(URL, Title, body,output_file): # csv 파일 형태로 저장
    temp = []
    temp.append(URL)
    temp.append(Title)
    temp.append(body)
    result.append(temp)
    # csv 저장
    f = open(f'{output_file}.csv', 'w', encoding='utf-8-sig', newline='')
    csvWriter = csv.writer(f)
    for i in result:
        csvWriter.writerow(i)# 한줄씩 써 내려감
    f.close()
    print('완료 되었습니다.')

def main(argv):
    if len(sys.argv) != 5:
        print("python [모듈이름] [키워드] [가져올 페이지 숫자] [결과 파일명]")
        print(sys.argv)
        return
    date1 = argv[1]
    date2 = argv[2]
    date = argv[1]+"to"+argv[2]
    keyword = argv[3]
    #page_num = int(argv[2])
    output_file_name = argv[4]
    target_URL = TARGET_URL_BEFORE_DATE +quote(date) + TARGET_URL_BEFORE_KEWORD + quote(keyword) + TARGET_URL_PAGE
    get_link_from_news_title(target_URL, output_file_name)


if __name__ == '__main__':
    main(sys.argv)
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
import warnings
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from pytube import YouTube
import re
import warnings
from datetime import timedelta
import pymysql
from sqlalchemy import create_engine
import sqlalchemy
warnings.filterwarnings(action='ignore')
import numpy as np

#< 함수 영역 >
#########################################################################################################

######## db에서 url 가져오기
def url_find_in_db(cd):
    mysqldb = pymysql.connect(user='root',password='1234',host='3.35.70.166', db='test',charset='utf8')
    curs = mysqldb.cursor()
        ############ DB에서 데이터 가져오기 ################
        
    curs = mysqldb.cursor()
    query2 = 'select st_n,st_cd,url from {}'.format(cd)
    curs.execute(query2)

    db_table = pd.DataFrame(curs.fetchall(), columns=['st_n','st_cd','url'])
    mysqldb.commit()
    mysqldb.close()
    return db_table

######## 생성된 DF랑 sql과 비교
def duplicate_url_chk(df,df_db):
    
    for url in df['url']:
        if len(df_db[df_db['url']==url].index)!=0:
            idx=df[df['url']==url].index
            df.drop(df.index[idx],axis=0,inplace=True)
            df.reset_index(drop=True,inplace=True)
#             print('지워짐')
    print('중복되는 url 제거')
    return df

###################### 한글 삭제 #######################
def parseText(testText):
    korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
       #한글삭제
    parseText= re.sub(korean, '', testText).replace(' ','')
    #
    print('------한글 정규화------')
    return int(parseText)
##################### TEXT 칼럼 태그 처리 ###################
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    print('-----태그 정규화-----')
    return cleantext

##################### DB에 insert ###################
def insertTOdb(df,ch_nm,val):
    if ch_nm== '한국경제tv':
        ch_nm='hk'
    elif ch_nm== '삼프로tv':
        ch_nm='sampro'
    else:
        ch_nm='suka'
    pymysql.install_as_MySQLdb()

    engine = create_engine("mysql+mysqldb://root:"+"1234"+"@3.35.70.166/test?charset=utf8",encoding='utf8')
    conn = engine.connect()

    table_nm = 'youtube_'+ch_nm+'_'+val
    print('-==table_nm==',table_nm)
    print(df)
    df.to_sql(name=table_nm, con=engine, if_exists='append',index = False,dtype = {
        'st_n':sqlalchemy.types.VARCHAR(10),
        'st_cd':sqlalchemy.types.VARCHAR(10),
         'ch_nm':sqlalchemy.types.VARCHAR(30),
        'date':sqlalchemy.types.VARCHAR(20),
        'title':sqlalchemy.types.TEXT(),
         'text':sqlalchemy.types.TEXT(),
        'views':sqlalchemy.types.INT(),
        'length':sqlalchemy.types.INT(),
        'description':sqlalchemy.types.TEXT(),
        'url':sqlalchemy.types.TEXT()
    })


# 검색 하기
#########################################################################################################
querys = {'하이닉스':'000660','LG화학':'051910','현대차':'005380',"삼성전자":'005930'}#
for youtube_ch_nm in [1,2,3]:
    for key, val in querys.items():
        keyword = key
        st_cd = val

        ### 한국경제
        if youtube_ch_nm == 1:
            url = 'https://www.youtube.com/c/hkwowtv/search?query={}'.format(keyword)
            ch_nm= '한국경제tv'
            db_table_name='youtube_hk_'            
            
        #삼프로tv
        elif youtube_ch_nm == 2:
            ch_nm= '삼프로tv'
            url = 'https://www.youtube.com/c/%EC%82%BC%ED%94%84%EB%A1%9Ctv/search?query={}'.format(keyword)
            db_table_name='youtube_sampro_'
        #  슈카월드
        else:
            ch_nm= '슈카월드'
            url = 'https://www.youtube.com/c/%EC%8A%88%EC%B9%B4%EC%9B%94%EB%93%9C/search?query={}'.format(keyword)
            db_table_name='youtube_suka_'

        ##########################################################################################################################
        chrome_options = webdriver.ChromeOptions()
        ############# DevToolsActivePort file doesn't exist error 해결법 #############
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_path = '/home/lab16/data/chromedriver'
        driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
        driver.get(url)

        scroll_pane_height = driver.execute_script('return document.documentElement.scrollHeight')
        ######## 스크룰 내리기 #################
        while True:
            driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight)')
            time.sleep(2)
            new_scroll_page_height = driver.execute_script('return document.documentElement.scrollHeight')
            print(scroll_pane_height,new_scroll_page_height)
            if scroll_pane_height == new_scroll_page_height:
                break
            scroll_pane_height = new_scroll_page_height


        soup = bs(driver.page_source, 'html.parser')

        driver.close()

        ###########################################################################################################
        youtubeDf = pd.DataFrame()


        name = soup.select('a#video-title')
        time.sleep(1)
        video_url = soup.select('a#video-title')
        time.sleep(1)
        view = soup.select('a#video-title')
        time.sleep(1)
        dates = soup.find_all('div',{'id':'metadata-line'})
        time.sleep(1)
        times=soup.find_all('span',{'class':'style-scope ytd-thumbnail-overlay-time-status-renderer'})

        name_list = []
        url_list = []
        view_list = []
        date_list=[]
        time_list = []

        ## 
        for i in range(len(name)):
            name_list.append(name[i].text.strip())
            view_list.append(view[i].get('aria-label').split()[-1])
            date_split=view[i].get('aria-label').split()
            try:
                date_index=date_split.index('ago') 
#                 ## ~~시간, 며칠 전
#                 ## 당일 자료 아님 넘김
#                 if '시간' in date_split[date_index-2:date_index][0]:
#                     date_list.append(date_split[date_index-2:date_index][0])
#                 ## ~~시간, 며칠 전
#                 ## 당일 자료 아님 넘김
#                 elif '1일' in date_split[date_index-2:date_index][0]:
#                     date_list.append(date_split[date_index-2:date_index][0])
#                 else:
#                     date_list.append(np.nan)
#                     continue
                ## ~~시간, 며칠 전
                ## 당일 자료 아님 넘김
                if 'hour' in "".join(date_split[date_index-2:date_index]):
                    date_list.append(date_split[date_index-2:date_index][0])
                ## ~~시간, 며칠 전
                ## 당일 자료 아님 넘김
                elif 'day' in "".join(date_split[date_index-2:date_index]):
                    date_list.append(date_split[date_index-2:date_index][0])
                else:
                    date_list.append(np.nan)
                    continue
            except:
                date_list.append(np.nan)
                continue
        ## URL 계산
        for i in video_url:
            url_list.append('{}{}'.format('https://www.youtube.com',i.get('href')))

        ## 재생 시간 
        for i in range(len(times)):
            if '실시간' in times[i].get('aria-label'):
                time_list.append(np.nan)
                continue
            time_list.append(times[i].get('aria-label'))

        youtubeDic = {
            'st_n':keyword, # 종목 명
            'st_cd':st_cd, # 종목 코드
            'ch_nm': ch_nm, # 채널명
            'date': '', # 계산된 날짜
            'title': name_list, #제먹
            'url': url_list, #url
            'cnt': view_list, #조회수
            'times':time_list, # 재생 시간
            'datess': date_list # 업로드 날짜
        }
        
        ####### 스크롤 내린 결과
        result= pd.DataFrame(youtubeDic)
        result.dropna(axis=0,inplace=True)
        result.drop_duplicates(inplace=True)
        result.reset_index(inplace=True)
        result.drop(columns='index',inplace=True)
        print(ch_nm,"-의 ",key,'--스크롤 끝--')
        ############ db 테이블 가져오기
#         db_table=url_find_in_db(db_table_name+val)
        ########### 스크롤한 DF랑 DB랑 비교
#         result=duplicate_url_chk(result,db_table)
        
####################################################################################################################################        
#### 내부 스크립트 가져오기
        # 크롤링 횟수 카운트
        a = 0
        youtubeDf_ss = pd.DataFrame(columns=['st_n','st_cd','ch_nm','title','text','views','length','description'])


        # while a<=ind:
        for i in range(len(result)):
#         for i in range(len(youtubeDf)):
            print('유튜브 스크립트 출력')
            print('{}번쨰'.format(a))
            dic={}
            try:
                video_url = result.loc[i,'url']
                yt = YouTube(video_url)
                yt.publish_date=yt.publish_date + timedelta(days=1)
                caption = yt.captions.get_by_language_code('a.ko')

                aa =str(caption.xml_captions)
                text=str(cleanhtml(aa)).replace('\n','')
                date=str(yt.publish_date).split(' ')[0].replace('-','')+'00'
                dic ={
                    'st_n':keyword,
                    'st_cd':st_cd,
                     'ch_nm':yt.author,
                    'date':date,
                    'title':yt.title,
                     'text':text,
                    'views':yt.views,
                    'length':yt.length,
                    'description':yt.description,
                   'url': result['url'][i]
                }
                
                youtubeDf_ss = youtubeDf_ss.append(pd.DataFrame.from_dict([dic]))
                youtubeDf_ss.reset_index(inplace=True)
                youtubeDf_ss.drop(columns=['index'],inplace=True)
                youtubeDf_ss.drop_duplicates(['text','title'],inplace=True)
                youtubeDf_ss.dropna(axis=0,inplace=True)
            except Exception as e:
                print('---except 발생---')
                print(e)
                continue
            a +=1
            
            ### DB에 insert
        try:
            insertTOdb(youtubeDf_ss,ch_nm,val)

        except:
            for i in range(len(youtubeDf_ss)):

                youtubeDf_ss['description'][i]=''.join(filter(str.isalnum, str(youtubeDf_ss['description'][i]))) 
            insertTOdb(youtubeDf_ss,ch_nm,val)
        
        print('========끝===========')
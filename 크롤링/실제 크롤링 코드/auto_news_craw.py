import sys, os
import requests
import selenium
from selenium import webdriver
import requests
from pandas import DataFrame
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import pickle, json, glob, time
from tqdm import tqdm
import pymysql
import warnings
# import MySQLdb
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import sqlalchemy
warnings.filterwarnings(action='ignore')
########################################## DB에 데이터 넣기 ################################################
def insertTOdb(news_df,press_nm,cd):
    if press_nm == '매일경제':
        press_nm = 'maeil'
    else:
        press_nm = 'asia'
    table_name=press_nm+'_news_craw_'+str(cd)
    news_df.to_sql(name=table_name, con=engine,if_exists='append',index = False,dtype = {
    'st_n':sqlalchemy.types.VARCHAR(10),
    'st_cd':sqlalchemy.types.VARCHAR(10),
    'news': sqlalchemy.types.TEXT(),
    'date':sqlalchemy.types.VARCHAR(20),
    'title' : sqlalchemy.types.TEXT(), 
    'url' :sqlalchemy.types.TEXT(),
    'text' : sqlalchemy.types.TEXT()

    })

    
################################################################  html 전체 전처리  #####################################
def cleanhtml(raw_html):
    try:
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = cleantext.replace('\n','')
        cleantext = cleantext.replace('\t','')
        cleantext=cleantext[cleantext.find('마의견'):cleantext.find('재배포 금지')]
    except:
        cleantext = '결과없음'
    print('html 클린')
    return cleantext

#####
################################################# 한 페이지 전체 읽기 ############################################################
def one_page_craw(url,query,cd,press_nm):
    browser.get(url)
    time.sleep(0.07)
    df_one_page_craw = pd.DataFrame()
    
    #페이지 수
#     page_ct=len(abc.find_elements_by_xpath('.//a'))
#     page_ct_tg = abc.find_elements_by_xpath('.//a')

# ####동적 제어로 페이지 넘어가며 크롤링
    news_dict = {}
    idx = 1
    cur_page = 1
    table = browser.find_element_by_xpath('//ul[@class="list_news"]')
    li_list = table.find_elements_by_xpath('./li[contains(@id, "sp_nws")]')
    news_num = len(li_list)
    news_df = pd.DataFrame()

    while idx < news_num:
        table = browser.find_element_by_xpath('//ul[@class="list_news"]')
        li_list = table.find_elements_by_xpath('./li[contains(@id, "sp_nws")]')
        area_list = [li.find_element_by_xpath('.//div[@class="news_area"]') for li in li_list]
        a_list = [area.find_element_by_xpath('.//a[@class="news_tit"]') for area in area_list]

        for n in a_list[:min(len(a_list), news_num-idx+1)]:
            n_url = n.get_attribute('href')

            news_sss = {'st_n':query,
                              'st_cd':cd,
                            'news': press_nm,
                            'date':str(crawling_main_text(n_url)[1]),
                              'title' : n.get_attribute('title'), 
                              'url' : n_url,
                              'text' : crawling_main_text(n_url)[0]}
            idx += 1
#             pbar.update(1)

            news_df=news_df.append(news_sss,ignore_index=True)
            
    return news_df



########################################### 언론사별 본문 위치 태그 파싱 함수 ############################################
print('본문 크롤링에 필요한 함수를 로딩하고 있습니다...\n' + '-' * 100)
def crawling_main_text(url):

    req = requests.get(url)
    req.encoding = None
    soup = BeautifulSoup(req.text, 'html.parser')
    dates=''
    res = []
    text=''
    # 연합뉴스
    if ('://yna' in url) | ('app.yonhapnews' in url): 
        main_article = soup.find('div', {'class':'story-news article'})
        if main_article == None:
            main_article = soup.find('div', {'class' : 'article-txt'})
            
        text = main_article.text
        
   ###### 전체 html로 수정 ######     
   # 매일경제, req.encoding = None 설정 필요
    elif 'mk.co' in url:
        try:
            text = soup.find('div', {'class' : 'art_txt'}).text
            text2 = soup.find('li', {'class' : 'lasttime'}).text
            dates = re.sub(r'[^0-9]', '', text2)[:10]
        except:
            try:
                text = soup.find('div', {'class' : 'view_txt'}).text
            except:
                text=cleanhtml(str(soup))
            try:
                text2 = soup.find('li', {'class' : 'lasttime'}).text
                dates = re.sub(r'[^0-9]', '', text2)[:10]
            except:
                text2 = '0'
#             dates = re.sub(r'[^0-9]', '', text2)

    # 매일경제, req.encoding = None 설정 필요
    elif 'biz.heraldcorp' in url:
        try:
            text = soup.find('div',{'class':'article_left'}).text.replace('\n','')
            dates = soup.find('li',{'class':'article_date'}).text.split(' ')[0].replace('.','-')[:10]
        except:
            text = cleanhtml(str(soup))
            dates= 0
    ## 머니투데이
    elif 'biz.heraldcorp' in url:
        try:
            text = soup.find('div',{'id':'article'}).text.replace('\n','')
            dates = soup.find('li',{'class':'date'}).text.split(' ')[0].replace('.','-')
        except:
            text = cleanhtml(str(soup))
            dates= 0
            
    ## 아시아
    elif 'asiae.co' in url:
        try:
            text = soup.find('div',{'class':'article fb-quotable'}).text.replace('\n','')
#             dates = soup.find('p',{'class':'user_data'}).text.split('\t')[0].split(' ')[1:3]
#             dates =" ".join(dates).split(':')[0].replace(' ','').replace('.','')
            dates = soup.find('p',{'class':'user_data'}).text
            dates = re.sub(r'[^0-9]', '', dates)
            dates=dates[:10]
        except:
            text = cleanhtml(str(soup))
            dates= 0
    # 그 외
    else:
        text == None
        dates == None
    ###### 전체 html로 수정 ######
#     try:
#         text=text.replace('\n','').replace('\r','').replace('<br>','').replace('\t','')
#     except:
#         text= None
    
    res.append(text)
    res.append(dates)
    return res
    
    

print('검색할 언론사 : {}'.format('아시아경제'))

#######################<  실행 파트 >##############################

pymysql.install_as_MySQLdb()
engine = create_engine("mysql+mysqldb://root:"+"1234"+"@3.35.70.166/test?charset=utf8", encoding='utf-8')
# engine = create_engine("mysql+mysqldb://root:"+"1234"+"@localhost/proj", encoding='utf8')
conn = engine.connect()
#########################################################################################################################
################### 브라우저를 켜고 검색 키워드 입력 ###################################################################
# querys = {"삼성전자":'005930','하이닉스':'000660','네이버':'035420','카카오':'035720','삼성바이오로직스':'207940',
#           'LG화학':'051910','현대차':'005380','셀트리온':'068270'}
# 'SDI':'006400'


querys= {"삼성전자":'005930','하이닉스':'000660','LG화학':'051910','현대차':'005380'}
press_nms=['매일경제','아시아경제']

# 데이터 프레임

###### 날짜 저장 ##########
## 현재 시간
a=str(datetime.now()-timedelta(days=1))
a = a[:a.rfind(':')].replace('-', '.')
a=a[:a.find(' ')]
a

sleep_sec =0.5
news_df = DataFrame(columns=['st_n','st_cd','news','date','title','url','text'])
for press_nm in press_nms:
    for query,cd in querys.items():
        print(' query,cd',query,cd)
        # 1 페이지
        cureent_nm = 1
        press_nm = press_nm
        print('\n' + '=' * 100 + '\n')

        print('브라우저를 실행시킵니다(자동 제어)\n')
        chrome_options = webdriver.ChromeOptions()
        ############# DevToolsActivePort file doesn't exist error 해결법 #############
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_path = './data/chromedriver'
        browser = webdriver.Chrome(chrome_path,chrome_options=chrome_options)

        news_url = 'https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&sort=0&photo=0& \
            field=0&pd=3&ds={}&de={}&start=1'.format(query,a,a)
        browser.get(news_url)
        time.sleep(sleep_sec)


        ######### 언론사 선택 및 confirm #####################
        print('설정한 언론사를 선택합니다.\n')

        bx_press = browser.find_element_by_xpath('//div[@role="listbox" and @class="api_group_option_sort _search_option_detail_wrap"]//li[@class="bx press"]')

        # 기준 두번 째(언론사 분류순) 클릭하고 오픈하기
        press_tablist = bx_press.find_elements_by_xpath('.//div[@role="tablist" and @class="option"]/a')
        press_tablist[1].click()
        time.sleep(sleep_sec)

        # 첫 번째 것(언론사 분류선택)
        bx_group = bx_press.find_elements_by_xpath('.//div[@class="api_select_option type_group _category_select_layer"]/div[@class="select_wrap _root"]')[0]

        press_kind_bx = bx_group.find_elements_by_xpath('.//div[@class="group_select _list_root"]')[0]
        press_kind_btn_list = press_kind_bx.find_elements_by_xpath('.//ul[@role="tablist" and @class="lst_item _ul"]/li/a')


    ###########################  언로사 클릭 ###########################################################################
        for press_kind_btn in press_kind_btn_list:

            # 언론사 종류를 순차적으로 클릭(좌측)
            press_kind_btn.click()
            time.sleep(sleep_sec)

            # 언론사선택(우측)
            press_slct_bx = bx_group.find_elements_by_xpath('.//div[@class="group_select _list_root"]')[1]
            # 언론사 선택할 수 있는 클릭 버튼
            press_slct_btn_list = press_slct_bx.find_elements_by_xpath('.//ul[@role="tablist" and @class="lst_item _ul"]/li/a')
            # 언론사 이름들 추출
            press_slct_btn_list_nm = [psl.text for psl in press_slct_btn_list]

            # 언론사 이름 : 언론사 클릭 버튼 인 딕셔너리 생성
            press_slct_btn_dict = dict(zip(press_slct_btn_list_nm, press_slct_btn_list))

            # 원하는 언론사가 해당 이름 안에 있는 경우
            # 1) 클릭하고
            # 2) 더이상 언론사분류선택 탐색 중지
            if press_nm in press_slct_btn_dict.keys():
                print('<{}> 카테고리에서 <{}>를 찾았으므로 탐색을 종료합니다'.format(press_kind_btn.text, press_nm))

                press_slct_btn_dict[press_nm].click()
                time.sleep(sleep_sec)

                break

        ################ 뉴스 크롤링 ########################

        news_df = DataFrame(columns=['st_n','st_cd','news','date','title','url','text'])
        print('\n크롤링을 시작합니다.')
        # ####동적 제어로 페이지 넘어가며 크롤링
        news_dict = {}
        idx = 1
        cur_page = 1
        news_dict = {}
        idx = 1
        cur_page = 1
        try:
            table = browser.find_element_by_xpath('//ul[@class="list_news"]')
            li_list = table.find_elements_by_xpath('.//a')
        
            # news_num은 10
            news_numss = len(li_list)
            abc = browser.find_element_by_xpath('//div[@class="sc_page_inner"]')

            #페이지 수
            page_ct=len(abc.find_elements_by_xpath('.//a'))
            page_ct_tg = abc.find_elements_by_xpath('.//a')
        except:
            continue
        ################# 한 페이지 전체 읽기 #######################
        urls=browser.current_url
        res=one_page_craw(urls,query,cd,press_nm)
        news_df=news_df.append(res,ignore_index=True)
#         print(news_df.head(1))
        news_df.drop_duplicates(['title'],inplace=True)
        news_df.dropna(axis=0,inplace=True)
        insertTOdb(news_df,press_nm,cd)
        news_df = DataFrame(columns=['st_n','st_cd','news','date','title','url','text'])

        ############### 다음 페이지 넘기기 ############################
        try:
            btn_next=browser.find_element_by_xpath('//a[@role="button" and @class="btn_next"]').get_attribute('href')
        except:
            continue
        print(btn_next)
        while btn_next != None:
            btn_next=browser.find_element_by_xpath('//a[@role="button" and @class="btn_next"]').get_attribute('href')
    #     while page_ct >cureent_nm:
            print('cureent_nm-----',cureent_nm)
            browser.find_element_by_xpath('//a[@role="button" and @class="btn_next"]').click()
            nxt_pg = browser.current_url
    #         nxt_pg= browser.current_url+'&start='+str(cureent_nm*10+1)
            #### 다음 페이지 이동 ####
            browser.get(nxt_pg)
            time.sleep(sleep_sec)
            urls=browser.current_url
            res=one_page_craw(urls,query,cd,press_nm)
            news_df=news_df.append(res,ignore_index=True)
            news_df.drop_duplicates(['title'],inplace=True)
            news_df.dropna(axis=0,inplace=True)
            cureent_nm += 1
            insertTOdb(news_df,press_nm,cd)
            news_df = DataFrame(columns=['st_n','st_cd','news','date','title','url','text'])

        ################################################################
        else:
            print('\n브라우저를 종료합니다.\n' + '=' * 100)
            time.sleep(0.3)

browser.close()
conn.close()
#     browser.close()
#     break
#### 데이터 전처리하기 ###################################################### 

print('데이터프레임 변환\n')
# news_df

# xlsx_file_name = '네이버뉴스_본문_{}.xlsx'.format('아시아경제_현대차_2020')

# news_df.to_excel(xlsx_file_name)

print('=' * 100 + '\n결과물의 일부')

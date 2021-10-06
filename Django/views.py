import json
from django.db import connection
import pandas as pd
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import json
import pandas as pd
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime,timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from wordcloud import WordCloud
from collections import Counter
import string
import random
import string

#################################################################################
## 유튜브
def youtube_pop(st_cd):
    cursor = connection.cursor()
    result_re = pd.DataFrame()
    finacedata = []

    if type(st_cd) == str:

        st_cd = [st_cd]
    else:
        st_cd = st_cd

    for cd in st_cd:
        # ############ DB에서 데이터 가져오기 ################
        query2 = 'SELECT * FROM `youtube_hk_{}` order by date desc limit 1;'.format(cd)
        result = cursor.execute(query2)
        globals()['youtube_hk_{}'.format(cd)] = pd.DataFrame(cursor.fetchall())

        result_re=result_re.append(globals()['youtube_hk_{}'.format(cd)])
        
    connection.commit()
    connection.close()
    for i in range(len(result_re)):
        row = {
            'st_n': result_re.iloc[i][0],
            'st_cd': result_re.iloc[i][1],
            'title': result_re.iloc[i][4],
            'url': result_re.iloc[i][5],
        }
        finacedata.append(row)
    newsJSON = json.dumps(finacedata)
    return newsJSON
#################################################################################
### 뉴스
def news_pop(st_cd,dates):

    dates='20210914'
    cursor = connection.cursor()
    result_re = pd.DataFrame()
    finacedata = []

    if type(st_cd) == str:

        st_cd = [st_cd]
    else:
        st_cd = st_cd

    for cd in st_cd:
        ## accuracy
        query2 = 'SELECT * FROM accuracy_point where st_nm = "{}" order by datetime desc,ratio desc limit 1;'.format(cd)
        result = cursor.execute(query2)
        if result == 0:
            dates = dates_search(cd)

            query2 = 'SELECT * FROM accuracy_point where st_nm = "{}" order by datetime desc, ratio desc limit 1;'.format(cd)
            cursor.execute(query2)
        globals()['accuracy_{}'.format(cd)] = pd.DataFrame(cursor.fetchall())
        result_re = result_re.append(globals()['accuracy_{}'.format(cd)])
    connection.commit()
    connection.close()
    for i in range(len(result_re)):
        row = {
            'st_cd': result_re.iloc[i][0],
            'st_n': result_re.iloc[i][1],
            'news': result_re.iloc[i][2],
            'datetime':result_re.iloc[i][3][:8],
            'title': result_re.iloc[i][4],
            'url': result_re.iloc[i][5],
            'Tokenization': result_re.iloc[i][6],
            'Positive_Score': str(result_re.iloc[i][7]),
            'Negative_Score': str(result_re.iloc[i][8]),
            'Ratio': str(round(result_re.iloc[i][9],)),
            'Rred': str(result_re.iloc[i][10]),
        }
        finacedata.append(row)
    newsJSON = json.dumps(finacedata)
    return newsJSON

########## 긍정 부정 판단 할 뉴스
def news_pop_neg(st_nm,dates):
    cursor = connection.cursor()
    result_re = pd.DataFrame()
    finacedata = []

    ## accuracy
    ## 매일경제
    query2 = 'SELECT * FROM accuracy_point where st_nm = "{}" and news="{}" and abs(Ratio-0.5) not in(0.5,0) order by datetime desc,abs(Ratio-0.5) desc limit 1;'.format(
        st_nm,'매일경제')

    result = cursor.execute(query2)
    globals()['accuracy_{}'.format(st_nm)] = pd.DataFrame(cursor.fetchall())
    result_re = result_re.append(globals()['accuracy_{}'.format(st_nm)])

    ## 아시아경제
    query3 = 'SELECT * FROM accuracy_point where st_nm = "{}" and news="{}" and abs(Ratio-0.5) not in(0.5,0) order by datetime desc,abs(Ratio-0.5) desc limit 1;'.format(
        st_nm, '아시아경제')

    cursor.execute(query3)
    globals()['accuracy_{}'.format(st_nm)] = pd.DataFrame(cursor.fetchall())
    result_re = result_re.append(globals()['accuracy_{}'.format(st_nm)])

    connection.commit()
    connection.close()
    for i in range(len(result_re)):
        row = {
            'st_cd': result_re.iloc[i][0],
            'st_n': result_re.iloc[i][1],
            'news': result_re.iloc[i][2],
            'datetime':result_re.iloc[i][3][:8],
            'title': result_re.iloc[i][4],
            'url': result_re.iloc[i][5],
            'Tokenization': result_re.iloc[i][6],
            'Positive_Score': str(result_re.iloc[i][7]),
            'Negative_Score': str(result_re.iloc[i][8]),
            'Ratio': str(round(result_re.iloc[i][9],2)),
            'Rred': str(result_re.iloc[i][10]),
        }
        finacedata.append(row)

    news_pop_negJSON = json.dumps(finacedata)

    return news_pop_negJSON




########################################################################################################
### 코스피 연도별 그래프
def result(request, yearid):
    finacedata = []
    result=kospi_search(request)

    if yearid != 0:
        yearid = str(yearid)
        result=result[result['Date'].str.contains(yearid)]
    else:
    
        for i in range(len(result)):
            result['Date'][i] = result['Date'][i][:7]
        result=result.groupby(['Date']).mean()
        result.reset_index(inplace=True)
    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0],
            'changes': str(round(result.iloc[i][1], 1))
        }
        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    return finacedataJSON
######################################################################################################
### 코스피 데이터 가져오기
def kospi_search(request):
    ############################## 데이터 칼럼 가져 오기
    cursor = connection.cursor()
    query1 = 'show full columns from `kospi`'
    cursor.execute(query1)
    select = pd.DataFrame(cursor.fetchall())
    col = list()
    for i in select[0]:
        col.append(i)

    query2 = 'SELECT * FROM `kospi`;'
    cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    return result

####################################################################################################################



#############################################################################
## 개별 종목
##
def finance_data(st_cd,yearid=0):
    finacedata = []
    ############################## 데이터 칼럼 가져 오기
    cursor = connection.cursor()
    query1 = 'show full columns from `financedata`'
    cursor.execute(query1)
    select = pd.DataFrame(cursor.fetchall())
    col = list()
    for i in select[0]:
        col.append(i)
    ############################## 데이터
    if yearid ==0:
        query2 = 'SELECT * FROM `financedata` where st_cd = "{}";'.format(st_cd)
        result = cursor.execute(query2)
        result = pd.DataFrame(cursor.fetchall(), columns=col)
        if yearid == 0:
            for i in range(len(result)):
                result['Date'][i] = result['Date'][i][:7]
            result = result.groupby(['Date']).mean()
            result.reset_index(inplace=True)
    else:
        query2 = 'SELECT * FROM `financedata` where st_cd = "{}" and date like "{}%";'.format(st_cd,yearid)
        result = cursor.execute(query2)
        result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][4], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)
    return finacedataJSON

##################################
#### 주가 그래프 데이터
def date_finance_data(st_cd):

    finacedata = []
    ############################## 데이터 칼럼 가져 오기
    cursor = connection.cursor()
    query2 = 'SELECT * FROM `financedata` where st_cd = "{}" order by Date desc limit 1;'.format(st_cd)

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall())
    connection.commit()
    connection.close()

    row = {
        'dates': result.iloc[0][0][:10],
        'close': str(result.iloc[0][4]),
        'volume': str(result.iloc[0][5]),
        'changes': str(round(result.iloc[0][6], 3))
    }
    finacedata.append(row)
    datefinacedataJSON = json.dumps(finacedata)
    return datefinacedataJSON

######################################################################################################################
### 워드 클라우드
def wordcloud_maker(request,st_cd,dates):
    ## DB 연결
    cursor = connection.cursor()
    
    ## index.html 워드클라우드
    if st_cd == '0':
        query2 = 'SELECT * FROM youtube_token order by datetime limit 1;'.format(dates)
        result = cursor.execute(query2)
        result = pd.DataFrame(cursor.fetchall())
    ## 개별 종목 워드클라우드
    else:
        query2 = "SELECT * FROM youtube_token where st_cd = {} order by datetime desc limit 1;".format(st_cd)
        result = cursor.execute(query2)
        result = pd.DataFrame(cursor.fetchall())
    connection.commit()
    connection.close()


    # 한글 형태소 분석하기

    # # 단어 숫자 세기
    li = []

    for i in range(len(result)):
        li.extend(result.loc[i][6].split(' '))

    count = Counter(li)
    tags = count.most_common()
    tags= dict(tags)


    for index, (key, value) in list(enumerate(tags.items())):
        if index >= 30:
            del tags[key]

    wordcloudJSON = json.dumps(tags)

    return wordcloudJSON

###########################################

## 날짜 검색
def dates_search(st_nm):
    cursor = connection.cursor()
    result_re = pd.DataFrame()
    finacedata = []

    if st_nm == 0:
        dates = "SELECT datetime FROM accuracy_point order by datetime desc limit 1;"
    else:
        dates = "SELECT datetime FROM accuracy_point where st_nm = '{}' order by datetime desc limit 1;".format(st_nm)
        if type(int(st_nm)):

            dates = "SELECT datetime FROM accuracy_point where st_cd like'%{}%' order by datetime desc limit 1;".format(
                st_nm)
        else:
            dates = "SELECT datetime FROM accuracy_point where st_nm = '{}' order by datetime desc limit 1;".format(
            st_nm)



    cursor.execute(dates)
    connection.commit()
    connection.close()
    dates = pd.DataFrame(cursor.fetchall())
    dates = str(dates[0][0])[:8]

    return dates
######################

## 사용자 기사 투표
def samsung_chk(request):
    # data = json.loads(request.body.decode('utf8'))
    cursor = connection.cursor()
    st_cd = request.GET.get('st_n',None)
    like_ip = request.GET.get('ip',None)
    like_chk = request.GET.get('like',None)
    news  = request.GET.get('news',None)
    likes = {
        'like_ip':like_ip,
        'like_chk':like_chk

    }
    chkJSON=json.dumps(likes)

    now = datetime.now().strftime('%Y-%m-%d')
    
    chk_value=''

    if like_chk != None:
        ## 업데이트
        now = datetime.now().strftime('%Y-%m-%d')
        chk_value_in_db = "SELECT chk FROM user_chk where st_cd like '%{}%' and ip = '{}' and date = '{}' and news = '{}';".format(
            st_cd, like_ip, now, news)
        cursor.execute(chk_value_in_db)
        chk = pd.DataFrame(cursor.fetchall())

        if len(chk) != 0:
            chk_value = "update user_chk set chk= '{}' where st_cd like '%{}%' and news='{}' and ip = '{}' and date = '{}';".format(like_chk,st_cd,news,like_ip, now)

        ## insert
        else:
            chk_value = "insert into user_chk(st_cd, news, ip, chk, date) values('{}','{}','{}','{}','{}');".format(st_cd,news,like_ip,like_chk,now)

    cursor.execute(chk_value)
    connection.commit()
    connection.close()
    return HttpResponse({'chkJSON':chkJSON}, content_type="application/json")

##########################################################################################################################################################
### index_분석결과
def index_accuracy(st_nm,dates):
    cursor = connection.cursor()
    result_re = pd.DataFrame()
    finacedata = []
    
    query2 = "SELECT date,mail_news,asia_news,sampro_youtube, hk_youtube, suka_youtube FROM analysis_result group by date limit 1;"

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall())
    connection.commit()
    connection.close()
    result_re = result_re.append(result)
    
    row = {
        'date': result_re.iloc[0][0],
        'maeil': str(round(result_re.iloc[0][1]*100,1)),
        'asia': str(round(result_re.iloc[0][2]*100,1)),
        'sampro': str(round(result_re.iloc[0][3]*100,1)),
        'hk': str(round(result_re.iloc[0][4]*100,1)),
        'suka': str(round(result_re.iloc[0][5]*100,1)),
    }
    finacedata.append(row)

    index_acc = json.dumps(finacedata)

    return index_acc
    
##########################################################################################################################################################
#### 분석 결과 표출
def analysis_result(st_n):
    cursor = connection.cursor()
    
    analysis_result ="SELECT bb.*, f.close FROM analysis_result as bb \
    left join financedata as f on bb.code = f.st_cd and bb.date = f.Date \
    where  bb.code ='{}' and not f.close is null order by date desc limit 1;".format(st_n)
    chk = cursor.execute(analysis_result)
    analysis_result = pd.DataFrame(cursor.fetchall())
    connection.commit()
    connection.close()

    row = {
        'date': str(analysis_result[1].values[0]),
        'lstm':str(analysis_result[2].values[0]),
        'arima':str(analysis_result[3].values[0]),
        'fbprophet':str(analysis_result[4].values[0]),
        'RL':str(analysis_result[5].values[0]),
        'maeil':str(round(analysis_result[6].values[0]*100,1)),
        'asia':str(round(analysis_result[8].values[0]*100,1)),
        'sampro':str(round(analysis_result[10].values[0]*100,1)),
        'hk':str(round(analysis_result[11].values[0]*100,1)),
        'suka':str(round(analysis_result[12].values[0]*100,1)),
        'up_ratio':str(analysis_result[15].values[0]),
        'close':str(analysis_result[17].values[0]),
        
    }

    analysisJSON = json.dumps(row)
    return analysisJSON


######################################################################################################################
### 페이지 부분

def index(request, yearid=0):
    # finacedataJSON = kospi_search(request)

    ##### 주가 데이터
    finacedataJSON=result(request, yearid)
    st_cd = ['000660','005380','005930','051910','068270']
    st_nm = ['삼성전자','하이닉스','현대차','LG화학','셀트리온']
    ###### 날짜
    dates=dates_search(0)
    row = {
        'date': dates
    }
    datess = json.dumps([row])

    ###### 뉴스
    newsJSON=news_pop(st_nm,dates)

    ##### 정확도
    # accuracyJson=accuracy(request,'0')
    accuracyJson=index_accuracy(0,dates)

    #### 워드클라우드
    wordcloudJSON=wordcloud_maker(request,'0',dates)

    return render(request,'index.html',{'finacedataJSON':finacedataJSON,'newsJSON':newsJSON,'accuracyJson':accuracyJson,'wordcloudJSON':wordcloudJSON,'dates':datess})

def samsung(request,yearid=0):
    st_cd= '005930'
    st_nm='삼성전자'
    st_n = '5930'

    ####
    finacedataJSON=finance_data(st_cd,yearid)
    datefinacedataJSON=date_finance_data(st_cd)

    ###### 날짜
    dates = dates_search(st_n)
    row = {
        'date': dates
    }
    datess = json.dumps([row])

    # newsJSON=news_pop(st_nm,dates)
    news_pop_negJSON=news_pop_neg(st_nm, dates)


    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n,dates)

    #### 분석결과 + 정확도
    analysisJSON=analysis_result(st_n)

    return render(request, 'samsung.html', {'finacedataJSON': finacedataJSON,'datefinacedataJSON':datefinacedataJSON,'wordcloudJSON':wordcloudJSON,'dates':datess,
                                            'news_pop_negJSON':news_pop_negJSON,'analysisJSON':analysisJSON})

def sk_hynicx(request,yearid=0):
    st_cd = '000660'
    st_n = '660'
    st_nm='하이닉스'
    finacedataJSON = finance_data(st_cd, yearid)
    datefinacedataJSON = date_finance_data(st_cd)

    ###### 날짜
    dates = dates_search(st_n)
    row = {
        'date': dates
    }
    datess = json.dumps([row])
    ### 뉴스
    news_pop_negJSON=news_pop_neg(st_nm, dates)
    
    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n,dates)

    #### 분석결과 + 정확도
    analysisJSON = analysis_result(st_n)

    return render(request, 'sk_hynicx.html',
                  {'finacedataJSON': finacedataJSON, 'datefinacedataJSON': datefinacedataJSON,'wordcloudJSON':wordcloudJSON,'dates':datess,
                   'analysisJSON':analysisJSON,'news_pop_negJSON':news_pop_negJSON})

def hyundai(request,yearid=0):
    st_cd = '005380'
    st_n = '5380'
    st_nm = '현대차'
    finacedataJSON = finance_data(st_cd, yearid)
    datefinacedataJSON = date_finance_data(st_cd)

    ###### 날짜
    dates = dates_search(st_n)
    row = {
        'date': dates
    }
    datess = json.dumps([row])
    
    ### 뉴스
    news_pop_negJSON = news_pop_neg(st_nm, dates)

    #
    # accuracyJson = index_accuracy(st_n, dates)

    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n,dates)

    #### 분석결과 + 정확도
    analysisJSON = analysis_result(st_n)
    return render(request, 'hyundai.html',
                  {'finacedataJSON': finacedataJSON, 'datefinacedataJSON': datefinacedataJSON, 'news_pop_negJSON': news_pop_negJSON,'dates':datess
                   ,'wordcloudJSON':wordcloudJSON,'analysisJSON':analysisJSON})

def lg_chem(request,yearid=0):
    st_cd = '051910'
    st_n = '51910'
    st_nm = 'LG화학'
    finacedataJSON = finance_data(st_cd, yearid)
    datefinacedataJSON = date_finance_data(st_cd)
    ###### 날짜
    dates = dates_search(st_n)
    row = {
        'date': dates
    }
    datess = json.dumps([row])

    ### 뉴스
    news_pop_negJSON = news_pop_neg(st_nm, dates)

    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n,dates)

    #### 분석결과 + 정확도
    analysisJSON = analysis_result(st_n)

    return render(request, 'lg_chem.html',
                  {'finacedataJSON': finacedataJSON, 'datefinacedataJSON': datefinacedataJSON, 'news_pop_negJSON': news_pop_negJSON,'dates':datess,
                   'analysisJSON':analysisJSON,'wordcloudJSON':wordcloudJSON})

def celltrion(request,yearid=0):
    st_cd = '068270'
    st_n = '68270'
    st_nm = '셀트리온'
    finacedataJSON = finance_data(st_cd, yearid)
    datefinacedataJSON = date_finance_data(st_cd)
    
    ###### 날짜
    dates = dates_search(st_n)
    row = {
        'date': dates
    }
    datess = json.dumps([row])

    ### 뉴스
    news_pop_negJSON = news_pop_neg(st_nm, dates)

    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n,dates)

    #### 분석결과 + 정확도
    analysisJSON = analysis_result(st_n)
    return render(request, 'celltrion.html',
                  {'finacedataJSON': finacedataJSON, 'datefinacedataJSON': datefinacedataJSON, 'news_pop_negJSON': news_pop_negJSON,'dates':datess,
                   'analysisJSON':analysisJSON,'wordcloudJSON':wordcloudJSON})


def charts(request):
    return render(request,'charts.html')

def charts_fin(request):
    return render(request,'charts_fin.html')



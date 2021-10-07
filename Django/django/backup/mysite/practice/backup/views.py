#from .models import Post
import json
from django.db import connection
import pandas as pd
# from .models import Post
import json

import pandas as pd
from django.db import connection
from django.shortcuts import render


# Create your views here.
def click_2018(request):
    print('2018')
    print('request',request)
    # index(request,'2018')
    # return render(request, 'index.html')
def result(self, request):
    print('2018')
    query = request.GET['query']
    print(self)
    return render(request, 'index.html')
def index(request):
    finacedata = []
    finacedata_dic = {}
    # try:
    ############################## 데이터 칼럼 가져 오기
    cursor = connection.cursor()
    # query1 = 'show full columns from `financedata`'
    query1 = 'show full columns from `kospi`'
    cursor.execute(query1)
    select = pd.DataFrame(cursor.fetchall())
    col = list()
    for i in select[0]:
        col.append(i)
    ############################## 데이터
    # query2 = 'SELECT * FROM `financedata` where st_cd = "000660";'

    query2 = 'SELECT * FROM `kospi`;'
    result=cursor.execute(query2)
    result=pd.DataFrame(cursor.fetchall(),columns=col)
    connection.commit()
    connection.close()
    print(result)
    for i in range(len(result)):
        result['Date'][i] = result['Date'][i][:7]
    result = result.groupby(['Date']).mean()[['Close']]
    result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
                'dates' : result.iloc[i][0],
               'changes': str(round(result.iloc[i][1],3))
            # ,
            # 'dates': result.iloc[i, 0]
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)
    print(finacedataJSON)
    return render(request,'index.html',{'finacedataJSON':finacedataJSON})

def samsung(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "005930";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    for i in range(len(result)):
        result['Date'][i] = result['Date'][i][:7]
    result = result.groupby(['Date']).mean()[['Close']]
    result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)
    print(finacedataJSON)
    return render(request, 'samsung.html', {'finacedataJSON': finacedataJSON})

def sk_hynicx(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "000660";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    # for i in range(len(result)):
    #     result['Date'][i] = result['Date'][i][:7]
    # result = result.groupby(['Date']).mean()[['Change']]
    # result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # print(finacedataJSON)
    return render(request,'sk_hynicx.html',{'finacedataJSON': finacedataJSON})

def hyundai(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "005380";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    # for i in range(len(result)):
    #     result['Date'][i] = result['Date'][i][:7]
    # result = result.groupby(['Date']).mean()[['Change']]
    # result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # print(finacedataJSON)
    return render(request, 'hyundai.html', {'finacedataJSON': finacedataJSON})

def lg_chem(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "051910";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    # for i in range(len(result)):
    #     result['Date'][i] = result['Date'][i][:7]
    # result = result.groupby(['Date']).mean()[['Change']]
    # result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # print(finacedataJSON)
    return render(request, 'lg_chem.html', {'finacedataJSON': finacedataJSON})

def celltrion(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "068270";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    # for i in range(len(result)):
    #     result['Date'][i] = result['Date'][i][:7]
    # result = result.groupby(['Date']).mean()[['Change']]
    # result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # print(finacedataJSON)
    return render(request, 'celltrion.html', {'finacedataJSON': finacedataJSON})
def charts(request):
    return render(request,'charts.html')



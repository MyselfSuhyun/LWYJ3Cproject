import requests
from .gecoder import GeoHelper
from .weatherhelper import WheeatherHelper
import pandas as pd
import datetime
import json
from numpy import NaN

# 좌표를 시,구,동 으로 변환해주는코드예요.
def test(y,x):
    geo = GeoHelper('99CA85DC-5065-3944-BA0F-4E160AB25F0D')
    select_url = geo.get_request_url(x,y)
    # print(select_url)
    geo_data = requests.get(select_url).json()
    result_data = geo_data['response']['result'][0]['text'].split()
    return result_data

# 제임스가했떤거, API로 저희 날씨랑 습도 가져오는거예요.
def weather(nx,ny,ym,hm,h):
    whe = WheeatherHelper('pi%2FMf18g2nh%2F4NkdE15T6OqL3pFDO1wZug83XDwIC6whRCxEeUAioAtYn8%2FraFQaJIugL%2FUof8KoFoGne%2FOwkA%3D%3D')
    choice = whe.get_request_dong(nx,ny,ym,hm)
    # print(choice)
    response = requests.get(choice).text
    data = json.loads(response) #json 문자열을 파이썬에서 사용할 수 있는 객체로 만들어줌
    tmp = 0
    hum = 0
    if h:
        for i in range(60):
            fcst = data['response']['body']['items']['item'][i]['fcstTime']
            san = data['response']['body']['items']['item'][i]['category']
            if san == 'T1H' and fcst == h and not tmp:
                tmp = data['response']['body']['items']['item'][i]['fcstValue']
            elif san == 'REH' and fcst == h and not hum:
                hum = data['response']['body']['items']['item'][i]['fcstValue']        
    else:
        for i in range(60):
            san = data['response']['body']['items']['item'][i]['category']
            if san == 'T1H' and not tmp:
                tmp = data['response']['body']['items']['item'][i]['fcstValue']

            elif san == 'REH' and not hum:
                hum = data['response']['body']['items']['item'][i]['fcstValue']
    return tmp,hum


# 제임스가 한거 엑셀읽어오는거!
def confirm():
    #엑셀 읽기
    a1 = pd.read_excel('gisangapi.xlsx', header=1, engine ='openpyxl')
    #읽은 엑셀을 리스트로변환
    alist = a1.values.tolist()
    gisang_dict = {}
    i=0
    #리스트에서 한 행씩 읽어서 str변수에 원하는 형태로 삽입
    while i<len(alist):
        if gisang_dict.get(alist[i][2]):
            if gisang_dict[alist[i][2]].get(alist[i][3]):
                if not alist[i][4] is NaN:
                    gisang_dict[alist[i][2]][alist[i][3]][alist[i][4]]=[alist[i][5],alist[i][6]]
                    i+=1
                else:
                    gisang_dict[alist[i][2]][alist[i][3]]['default']=[alist[i][5],alist[i][6]]
                    i+=1
            else:
                gisang_dict[alist[i][2]][alist[i][3]]={alist[i][4]:''}
        else:
            gisang_dict[alist[i][2]]={alist[i][3]:''}
    return gisang_dict
        
# def send(long,lati):
#     dic_j = confirm() # 기상 정보를 가져오기위한 격자를 보관한 딕셔너리 받아오기!
#     # long,lati = map(float,input().split()) # 위도, 경도를 입력받는거.
#     dong = test(float(long),float(lati))
#     # print(dong)
#     # print(dic_j)
#     if dic_j.get(dong[0]):
#         if dic_j[dong[0]].get(dong[1]):
#             if dic_j[dong[0]][dong[1]].get(dong[2]):
#                 dic_url = dic_j[dong[0]][dong[1]][dong[2]]
#             else:
#                 dic_url = dic_j[dong[0]][dong[1]]['default']
#     # print(dic_url)

    # hellotime=0
    # now = datetime.datetime.now()
    # nowDate = now.strftime('%Y%m%d')
    # nowtime = int(now.strftime('%H%M'))-100
    # resulttime = now.strftime('%H:%M')
    # if nowtime<100:
    #     nowtime=f'00{nowtime}'
    # elif nowtime<1000:
    #     nowtime = f'0{nowtime}'
    # elif nowtime>=1800:
    #     nowtime = 1700
    #     hellotime = now.strftime('%H')+'00'


#     temp, human = weather(dic_url[0],dic_url[1],nowDate,nowtime,hellotime)
#     # print(f'현재위치 {dong[2]}이며, 현재 시간 {resulttime}입니다.  기온은 {temp}°이며, 습도는 {human}% 입니다.')
#     result = [dong[2],int(temp),int(human)]
#     return result

def send(long,lati):
    # long,lati = map(float,input().split()) # 위도, 경도를 입력받는거.
    dong = test(float(long),float(lati))
    return dong

def gisangapi(dong,gridx,gridy):
    hellotime=0
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    nowtime = int(now.strftime('%H%M'))-100
    resulttime = now.strftime('%H:%M')
    if nowtime<100:
        nowtime=f'00{nowtime}'
    elif nowtime<1000:
        nowtime = f'0{nowtime}'
    elif nowtime>=1800:
        nowtime = 1700
        hellotime = now.strftime('%H')+'00'
    temp, human = weather(gridx,gridy,nowDate,nowtime,hellotime)
    # print(f'현재위치 {dong[2]}이며, 현재 시간 {resulttime}입니다.  기온은 {temp}°이며, 습도는 {human}% 입니다.')
    result = [dong, int(temp),int(human)]
    return result

def error(tem,hum):
    result = []
    result.append(int(tem))
    result.append(int(hum))
    return result
import requests
import json

class WheeatherHelper:
    def __init__(self, api_key=None):
        self.api_key = api_key


    def get_request_dong(self,nx,ny,ym,hm):

        numOfRows='60'
        pageNo = '1'

        dataType='JSON'
        url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={self.api_key}&numOfRows={numOfRows}&pageNo={pageNo}&base_date={ym}&base_time={hm}&nx={nx}&ny={ny}&dataType={dataType}'

        return url
    

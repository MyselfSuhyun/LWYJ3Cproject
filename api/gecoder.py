import requests

class GeoHelper:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def get_request_url(self,longitude,latitude):
        base_url = 'http://api.vworld.kr/req/address?service=address&request=getAddress&version=2.0&crs=epsg:4326&point='
        request_url = base_url + f'{longitude},{latitude}&format=json&type=both&zipcode=true&simple=false'
        request_url += f'&key={self.api_key}'

        return request_url
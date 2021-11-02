import serial
import webbrowser

def solve(li, lo, tm, hm):
    longitude = li  # 경도
    latitude = lo   # 위도
    temperature = tm
    humidity = hm

    url = f'http://127.0.0.1:8000/boards/search/?longitude={longitude}&latitude={latitude}&temperature={temperature}&humidity={humidity}'
    webbrowser.open(url)
    
    return data_list

_port = 'COM5'
_baud = 115200  # baudRate 통신속도, Bits Per Second 초당 비트수
ardu = serial.Serial(_port, _baud)  # 데이터 받아오는 부분

getData=str(ardu.readline())
data=getData[2:-5]      # 데이터 자르기 b/r 이상한값이 붙어서옴
data_list = list(map(float, data.split(',')))
solve(data_list[0], data_list[1], int(data_list[2]), int(data_list[3]))


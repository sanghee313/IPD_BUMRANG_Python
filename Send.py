import serial 
import time
import requests
from bs4 import BeautifulSoup

#print(Wolpyeong_chroline)
#print(Wolpyeong_pH)
#print(Wolpyeong_NTU)
#print()
#print(songchon_chroline)
#print(songchon_pH)
#print(songchon_NTU)
#print()
#print(shintanjin_chroline)
#print(shintanjin_pH)
#print(shintanjin_NTU)
#print()

py_serial = serial.Serial(
    #Window
    port ='COM8',

    # 보드 레이트(통신 속도)
    baudrate = 9600,

)

#아두이노랑 같이 실행시 Serial Monitor 꺼야함
while True:

    response = requests.get("http://www.waterworks.daejeon.kr/wps/std/main.do")
    html_data = BeautifulSoup(response.text,"html.parser")
    
    #css 선택
    w_c = html_data.find(id="DJ0103RC00")
    w_pH = html_data.find(id="DJ0103PH00")
    w_NTU = html_data.find(id="DJ0103TURB")
    
    s_c = html_data.find(id="DJ0302RC00")
    s_pH = html_data.find(id="DJ0302PH00")
    s_NTU = html_data.find(id="DJ0302TURB")
    
    shin_chroline = html_data.find(id="DJ0201RC00")
    shin_pH = html_data.find(id="DJ0201PH00")
    shin_NTU = html_data.find(id="DJ0201TURB")
    
    #str 추출 
    Wolpyeong_chroline = w_c.get_text()
    Wolpyeong_pH = w_pH.get_text()
    Wolpyeong_NTU = w_NTU.get_text()
    
    songchon_chroline = s_c.get_text()
    songchon_pH = s_pH.get_text()
    songchon_NTU = s_NTU.get_text()
    
    shintanjin_chroline = shin_chroline.get_text()
    shintanjin_pH = shin_pH.get_text()
    shintanjin_NTU = shin_NTU.get_text()
      
    #commend = input('아두이노에게 내릴 명령:')
    
    #py_serial.write(commend.encode())
    
    #time.sleep(0.1)
    
    if py_serial.readable():
        
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        #response = py_serial.readline()
        tubility_data = py_serial.readline() #습도 데이터 받음 
        celcius_data = py_serial.readline()  #온도 데이터 받음 
        
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        #print(response[:len(response)-1].decode())
        print(tubility_data[:len(tubility_data)-1].decode()) #타입 str
        print(celcius_data[:len(celcius_data)-1].decode())   #타입 str

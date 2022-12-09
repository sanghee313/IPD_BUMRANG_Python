# rasberry pi 필수 설치 
# pip 설치 
# pip install bs4 (BeautifulSoup)
# sudo pip install firebase-admin

import serial 
import time
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('firebase-sdk.json')

firebase_admin.initialize_app(cred, {
	'databaseURL' : 'https://bumrang-36405-default-rtdb.asia-southeast1.firebasedatabase.app'
})

##데이터 베이스 초기 설정 
#ref =db.reference('/')
#ref.set({
#
#    "Total_Data" :  {
#            "Wolpyeongdong" : {
#                "chroline" : "0",
#                "pH" : "0",
#                "NTU" : "0"
#            },
#            "songchondong" : {
#                "chroline" : "0",
#                "pH" : "0",
#                "NTU" : "0"
#            },
#            "shintanjin" : {
#                "chroline" : "0",
#                "pH" : "0",
#                "NTU" : "0"
#            },
#            "semisosa" : {
#                "tubility" : "0",
#                "temperature" : "0"
#            }
#        }
#})

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

    print("월평동 정수장 ")
    print(Wolpyeong_chroline)
    print(Wolpyeong_pH)
    print(Wolpyeong_NTU)
    print("송촌동 정수장 ")
    print(songchon_chroline)
    print(songchon_pH)
    print(songchon_NTU)
    print("신탄진 정수장")
    print(shintanjin_chroline)
    print(shintanjin_pH)
    print(shintanjin_NTU)
    print()    
    
    if py_serial.readable():
        
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        #response = py_serial.readline()
        tubility_data = py_serial.readline() #습도 데이터 받음 
        temperature_data = py_serial.readline()  #온도 데이터 받음 
        
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        #print(response[:len(response)-1].decode())
        print(tubility_data[:len(tubility_data)-1].decode()) #타입 str
        print(temperature_data[:len(temperature_data)-1].decode())   #타입 str
        
        #디코딩한 값 저장 
        semisosa_tubility = tubility_data[:len(tubility_data)-1].decode()
        semisosa_temperature = temperature_data[:len(temperature_data)-1].decode()

    #updating data
    ref =db.reference("Total_Data")
    ref.update({
        
        #월평동 데이터 갱신
        "Wolpyeongdong/chroline":Wolpyeong_chroline,
        "Wolpyeongdong/pH":Wolpyeong_pH,
        "Wolpyeongdong/NTU":Wolpyeong_NTU,

        #신탄진 데이터 갱신 
        "shintanjin/chroline": shintanjin_chroline,
        "shintanjin/NTU": shintanjin_NTU,
        "shintanjin/pH": shintanjin_pH,

        #송촌동 데이터 갱신 
        "songchondong/chroline": songchon_chroline,
        "songchondong/NTU":songchon_NTU,
        "songchondong/pH":songchon_pH,
        
        #음수대[세미소사] 데이터 갱신 
        "semisosa/tubility" :semisosa_tubility,
        "semisosa/temperature" : semisosa_temperature
    })
    
    #5초마다 데이터 갱신 
    time.sleep(5) 


import serial 
import time

py_serial = serial.Serial(
    #Window
    port ='COM8',

    # 보드 레이트(통신 속도)
    baudrate = 9600,

)

#아두이노랑 같이 실행시 Serial Monitor 꺼야함
while True:
      
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


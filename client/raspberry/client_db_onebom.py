# -*- coding: utf8 -*-
import cv2          # opencv 패키지 import
import socket       # socekt 통신 패키지 import
import numpy as np  # numpy  패키지 import
import pymysql      # maria DB 패키지 import
import os           # Operating System, 운영체제와 상호작용 하는 패키지 import
import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial('/dev/serial0', 115200)
ser.close()
ser.open()

## TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 소켓 객체 생성. 패밀리 : AF_INET : IP4v, 타입 : SOCK_STREAM
s.connect(('10.2.52.51', 8896)) # 소켓 통신 연결 (server ip, port) 연구실
## s.connect(('192.168.0.56', 8896)) # 소켓 통신 연결 (server ip, port) ASUS
## s.connect(('192.168.0.60', 8896)) # 소켓 통신 연결 (server ip, port) LG

## Maria DB 연결
db = pymysql.connect(host='192.168.0.63', user='root', password='pi', db='mysql', charset='utf8')
cur = db.cursor()

## webcam 이미지 capture
cam = cv2.VideoCapture(0) # 카메라 열기. 0은 기본카메라(장치관리자 저장 순서).
print('capture image')
cam.set(3, 608);          # 이미지 속성 변경 3 = width, 4 = height
cam.set(4, 608);


speed = "SELECT MOTORLENGTH FROM motor ORDER BY DATETIME DESC LIMIT 1"
cur.execute(speed)
result = cur.fetchall()
speed = result[0][0]
pre_speed = speed
db.commit()

## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
while True:
    # 비디오의 한 프레임씩 읽는다.
    # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
    ret, frame = cam.read()
    if ret == False:
        print('ret False')
        if cam.isOpened() == False:
            print('cam.isOpened == False')
            cam.open
            print('cam.open')

    # cv2.imencode(ext, img , [params])
    # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
    result, frame = cv2.imencode('.jpg', frame, encode_param)

    # frame을 String 형태로 변환
    data = np.array(frame)         # frame을 numpy 배열 형태로 변환
    stringData = data.tobytes()    # numpy 배열 데이터를 byte형태 binary 형태로 변환

    #서버에 stringData 정보 전송
    #(str(len(stringData))).encode().ljust(16)
    # sendall()이 send()보다 속도가 비교적 느리지만 안정.
    # ljust(n, c=''): 문자열을 왼쪽으로 n만큼 정렬
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)

    #---------------------Server 에서 예측된 count 값을 return -------------------#
    count=s.recv(1024).decode("utf-8") # 쿼리 문자열에서 검색하기 위해 utf-8로 변환

    sql = "INSERT INTO counting(counting) VALUES (%s)" %count
    cur.execute(sql)
    print("Count: " + count)
    db.commit()

    speed = "SELECT MOTORLENGTH FROM motor ORDER BY DATETIME DESC LIMIT 1"
    cur.execute(speed)
    result = cur.fetchall()
    speed = result[0][0]
    if pre_speed != speed:
        ser.write(speed.encode())
        pre_speed = speed
        print("change speed: " + pre_speed)
    print("Speed: " + speed)
    print('\n')
    db.commit()

print('EXIT')
db.close()
ser.close()
cam.release()
client_socekt.close()

import socket
import cv2
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1" # Server의 GPU 사용 번호
import numpy as np
from sort import Sort                    # 배열의 요소를 적절한 위치에 정렬 후 반환
from object_counting_api import ObjectCountingAPI
from PIL import Image                    # 이미지 분석 및 처리 라이브러리
from darkflow.net.build import TFNet
from utils import COLORS, intersect, get_output_fps_height_and_width # small Python functions and classes which make common patterns shorter and easier
from flask import Flask
from flask import request
from flask import Response
from flask import

from flask import render_template
from queue import Queue # FIFO
import threading        # 코드 병렬 실행

#socket을 통해 라즈베리파이로부터 이미지를 받아오고, 서버에서 딥러닝을 거친 출력 결과(이미지)를 flask 통신으로 웹으로 전송

#socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    buf = b''    # byte 문자열
    while count: # 0이 아닐경우 무한 반복
        newbuf = sock.recv(count)
        if not newbuf:return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def fps(self):

    self.current_time = time.time()
    self.sec = self.current_time - self.preview_time
    self.preview_time = self.current_time

    if self.sec > 0 :
        fps = round(1/(self.sec),1)
    else :
        fps = 1
    return fps

#라즈베리파이로부터 이미지 받는 서버 주소, 포트가 사용 중이라는 에러 뜨면 포트만 바꿔주면 됨
HOST='10.2.52.51'
PORT=8896

#TCP 사용
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # 최초의 수신자. 소켓을 만들고 포트에 맵핑한 다음, 클라이언트가 접속하기를 기다림.
print('Socket created')

#서버의 아이피와 포트번호 지정
s.bind((HOST,PORT)) # 바인딩 : 서버가 소켓을 포트에 맵핑하는 행위
print('Socket bind complete')

# 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
s.listen(10)
print('Socket now listening')

# 연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소정보
conn,addr=s.accept()

# 사용하는 딥러닝 모델의 옵션, 아래 counting하는 알고리즘에서 사용
# load에는 사용하는 모델의 ckpt 숫자(yolo-new-6120), threshold에는 얼마나 엄격하게 라벨 값을 잡아낼 건지에 대한 기준치, gpu는 gpu 사용
options = {"model": "cfg/yolo-new.cfg", "load": 6120, "threshold": 0.65, "gpu": 1.0}
counter = ObjectCountingAPI(options)

tracker = Sort()
memory = {}
count = 1

#--------------------------------- flask 통신 시작
app = Flask( __name__ )
    # ,render_template("Web dev.html", result="나 여기")

@app.route('/stream')
def stream():
    return Response(stream_with_context(stream_gen()), mimetype='multipart/x-mixed-replace; boundary=frame')
    #mimetype="text/event=stream"

def stream_gen():
    global count
    while True:
        length = recvall(conn, 16)
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype = 'uint8')
        count+=1
        #data를 디코딩한다.
        frame2 = cv2.imdecode(data, cv2.IMREAD_COLOR)
        # 받아온 frame을 딥러닝에 입력 값으로 줌, counting하기 위해 필요한 변수들과 line 위치를 지정
        aa=counter.count_objects_on_image(count,frame2, tracker, memory, line_begin=(100, 210), line_end=(508, 210), output_path="./the_output.avi", show=True)
        frame2 = cv2.imencode('.jpg', frame2 )[1].tobytes()
        conn.send(bytes(str(aa),"utf-8"))

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')


if __name__ == '__main__' :
    print('connect to web...')
    app.run( host='0.0.0.0', port=3000,threaded=True)

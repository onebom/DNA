import socket
import cv2
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
import numpy as np
from sort import Sort
from object_counting_api import ObjectCountingAPI
from PIL import Image
from darkflow.net.build import TFNet
from utils import COLORS, intersect, get_output_fps_height_and_width
from flask import Flask
from flask import request
from flask import Response
from flask import stream_with_context
from flask import render_template
from queue import Queue
import threading

#socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def fps(self):
    print('10')

    self.current_time = time.time()
    self.sec = self.current_time - self.preview_time
    self.preview_time = self.current_time

    if self.sec > 0 :
        fps = round(1/(self.sec),1)

    else :
        fps = 1

    return fps

HOST='10.2.52.53'
PORT=8891

#TCP 사용
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

#서버의 아이피와 포트번호 지정
s.bind((HOST,PORT))
print('Socket bind complete')
# 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
s.listen(10)
print('Socket now listening')

#연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
conn,addr=s.accept()


options = {"model": "cfg/tiny-yolo-voc-2.cfg", "load": -1, "threshold": 0.65, "gpu": 1.0}
counter = ObjectCountingAPI(options)

tracker = Sort()
memory = {}
count = 1

app = Flask( __name__ )
@app.route('/')
def html():
    return render_template("Web dev.html")

    # ,render_template("Web dev.html", result="나 여기")
@app.route('/stream')
def stream():
    return Response(stream_with_context( stream_gen()), mimetype='multipart/x-mixed-replace; boundary=frame')
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
        counter.count_objects_on_image(count,frame2, tracker, memory, line_begin=(170, 230), line_end=(360, 230), show=False)
        frame2 = cv2.imencode('.jpg', frame2 )[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')

# @app.route('/counting',  methods=['GET'])
# def counting():
#     count2 = 1
#     while True:
#         length = recvall(conn, 16)
#         stringData = recvall(conn, int(length))
#         data = np.fromstring(stringData, dtype = 'uint8')
#         count2+=1
#         #data를 디코딩한다.
#         frame2 = cv2.imdecode(data, cv2.IMREAD_COLOR)
#         count_num=counter.count_objects_on_image(count2,frame2, tracker, memory, line_begin=(170, 230), line_end=(360, 230), show=False)
#         yield {count2}
#         timr.sleep(1)
#         return render_template("Web dev.html", result=count2)
        # return render_template("Web dev.html", result=count2)



# @app.route('/')
# def count():
#     global count
#     while True:
#         length = recvall(conn, 16)
#         stringData = recvall(conn, int(length))
#         data = np.fromstring(stringData, dtype = 'uint8')
#         count+=1
#         #data를 디코딩한다.
#         frame2 = cv2.imdecode(data, cv2.IMREAD_COLOR)
#         count_num=counter.count_objects_on_image(count,frame2, tracker, memory, line_begin=(170, 230), line_end=(360, 230), show=False)
#
#         return render_template("Web dev.html", result="count_num")

if __name__ == '__main__' :
    print('connect to web...')
    app.run( host='0.0.0.0', port=5000,threaded=True)

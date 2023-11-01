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
from queue import Queue

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

# def bytescode(self,frame):
#     return cv2.imencode('.jpg', frame )[1].tobytes()

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
# count_num = 0
count = 1

    # cv2.imshow('frame', frame2)
    # cv2.waitKey(1)

app2 = Flask( __name__ )
@app2.route('/stream')
def stream():
    print('1')
    # global count

        #client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))


        #counter.count_objects_on_image(count,frame2, tracker, memory, line_begin=(170, 230), line_end=(350, 230), show=False)
        #counter.count_objects_crossing_the_virtual_line(frame, line_begin=(100, 170), line_end=(300, 170), show=True)
        # cv2.imshow('ImageWindow',frame)
        # cv2.imshow('frame', frame2)
        # cv2.waitKey(1)
        # Queue(maxsize=128).put(frame2)

        # frame2 = request.args.get( 'frame2', default = 0, type = int )
        #
        # print('im here!')
        # print(stream_gen( frame2 ))

    return Response(stream_with_context( stream_gen() ), mimetype='multipart/x-mixed-replace; boundary=frame' )

def stream_gen(  ):
    print('2')
    global count
    while True:
        length = recvall(conn, 16)
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype = 'uint8')
        count+=1
        #data를 디코딩한다.
        frame2 = cv2.imdecode(data, cv2.IMREAD_COLOR)
        counter.count_objects_on_image(count,frame2, tracker, memory, line_begin=(170, 230), line_end=(350, 230), show=False)
        frame2 = cv2.imencode('.jpg', frame2 )[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')

    # frame2 = streamer.bytescode(frame2)
    # yield (b'--frame\r\n'
    #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__' :
    print('connect to web...')
    app2.run( host='0.0.0.0', port=5000,threaded=True) #, debug=True, threaded=True, use_reloader=False)

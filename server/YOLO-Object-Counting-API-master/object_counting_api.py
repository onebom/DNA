from darkflow.net.build import TFNet
from sort import Sort
from utils import COLORS, intersect, get_output_fps_height_and_width
import cv2
import numpy as np
import time
import datetime
import threading
from datetime import timedelta
from flask import render_template


width=0
height=0
# 지정된 면적 이하의 사각형만 count한다. (물방울이 떨어질수록 면적이 큰 사각형이 잡히기 때문)
area1=0
area2=369664 # 608x608
DETECTION_FRAME_THICKNESS = 1 #선 굵기

OBJECTS_ON_FRAME_COUNTER_FONT = cv2.FONT_HERSHEY_SIMPLEX
OBJECTS_ON_FRAME_COUNTER_FONT_SIZE = 0.5


LINE_COLOR = (0, 0, 255)
sky_COLOR = (223,188,80)
LINE_THICKNESS = 2
#counter 옵션
LINE_COUNTER_FONT = cv2.FONT_HERSHEY_DUPLEX
LINE_COUNTER_FONT_SIZE = 0.7
LINE_COUNTER_POSITION = (20,45)
LINE_COUNTER_POSITION2= (20,85)


class ObjectCountingAPI:

    def __init__(self, options):
        self.options = options
        self.tfnet = TFNet(options)
        self.current_time = time.time()
        self.preview_time = time.time()
        self.sec = 0

    def _convert_detections_into_list_of_tuples_and_count_quantity_of_each_label(self, objects):
        labels_quantities_dic = {}
        results = []

        for object in objects:
            x1, y1 = object["topleft"]["x"], object["topleft"]["y"]
            x2, y2 = object["bottomright"]["x"], object["bottomright"]["y"]
            confidence = object["confidence"]
            label = object["label"]

            try:
                labels_quantities_dic[label] += 1
            except KeyError:
                labels_quantities_dic[label] = 1

            start_point = (x1, y1)
            end_point = (x2, y2)

            results.append((start_point, end_point, label, confidence))
        return results, labels_quantities_dic

    # 이 함수만 사용
    def count_objects_on_image(self, count, frame,  tracker, memory, line_begin, line_end, targeted_classes=[], output_path="./the_output.avi", show=True):

        line = [line_begin, line_end]
        objects = self.tfnet.return_predict(np.array(frame))

        if targeted_classes:
            objects = list(filter(lambda res: res["label"] in targeted_classes, objects))

        results, _ = self._convert_detections_into_list_of_tuples_and_count_quantity_of_each_label(
            objects)

        # convert to format required for dets [x1, y1, x2, y2, confidence]
        dets = [[*start_point, *end_point] for (start_point, end_point, label, confidence) in results]

        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(100)})
        dets = np.asarray(dets)
        tracks = tracker.update(dets)

        boxes = []
        indexIDs = []
        tracker = Sort()
        previous = memory.copy()
        memory = {}

        for track in tracks:
            boxes.append([track[0], track[1], track[2], track[3]]) # .append() 선택 요소의 내용의 끝에 컨텐트 추가
            indexIDs.append(int(track[4]))
            memory[indexIDs[-1]] = boxes[-1]

        global count_num
        global area1, area2
        if count ==2:
            count_num=0

        if len(boxes) > 0:
            # print('true')
            i = int(0)
            for box in boxes:
                (x, y) = (int(box[0]), int(box[1]))
                (w, h) = (int(box[2]), int(box[3]))

                # color = [int(c) for c in COLORS[indexIDs[i] % len(COLORS)]]
                color = (255,255,255)
                cv2.rectangle(frame, (x, y), (w, h), color, DETECTION_FRAME_THICKNESS) # 기존 frame에 rectangle 표시
                area1=abs((w-x)*(h-y))  # area1의 면적

                # 새로운 물방울에 대한 감지가 시작될 때 영역을 초기화해줌
                if area1<area2:
                    area2=369664

                p0=(int(x),int(y+(h-y)))
                p1=(int(x + (w-x)), int(y+(h-y))) # p0(x,h) ----------------- p1(w,h) 같은 높이
                #print(p0, p1)
                cv2.line(frame, p0, p1, color, 2)

                # p0[1]가 감지한 물방울 박스의 아래 선 y좌표
                # p0[1]이 빨간색 라인과 거기서부터 아래로 7픽셀 사이에 위치하고, 그 이전에 counting한 박스 크기보다 크지 않으면 counting (하나의 물방울에 대해 여러 번 counting하지 않도록 하기 위함)
                # line[0][1]: 라인의 h 좌표, p0[1]: 박스의 h좌표
                if line[0][1] <= p0[1] <= line[0][1] + 7 and area1 <= area2:
                    count_num += 1
                    area2=abs((w-x)*(h-y))

                # drop 라벨 값을 달아줌
                text = "{}".format('drop')
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                i += 1

        cv2.line(frame, line[0], line[1], LINE_COLOR, LINE_THICKNESS)

        cv2.putText(frame, 'COUNT: {}'.format(count_num), LINE_COUNTER_POSITION, LINE_COUNTER_FONT, LINE_COUNTER_FONT_SIZE,
                    sky_COLOR, 2)

        # self.current_time = time.time()
        # self.sec = self.current_time - self.preview_time
        # self.preview_time = self.current_time

        # if self.sec > 0 :
        #     fps = round(1/(self.sec),1)

        # else :
        #     fps = 1

        # line = [line_begin, line_end]

        # cv2.putText(frame, 'FPS: {0:.2f}'.format(fps), LINE_COUNTER_POSITION2, LINE_COUNTER_FONT, LINE_COUNTER_FONT_SIZE,sky_COLOR, 2)
        # cv2.waitKey(int(1000/fps))

        # return render_template("Web dev.html", result=count_num)

        return count_num

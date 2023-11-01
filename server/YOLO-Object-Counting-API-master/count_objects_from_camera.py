import cv2
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "3"
from object_counting_api import ObjectCountingAPI

options = {"model": "cfg/tiny-yolo-voc-2.cfg", "load": -1, "threshold": 0.65, "gpu": 1.0}



# cap = cv2.VideoCapture(VIDEO_PATH)
cap = cv2.VideoCapture(0) #real-time video

counter = ObjectCountingAPI(options)
# Draw framerate in corner of frame
cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)

counter.count_objects_on_video(cap, show=True)

import cv2
from object_counting_api import ObjectCountingAPI

options = {"model": "cfg/tiny-yolo-voc-2.cfg", "load": -1, "threshold": 0.65, "gpu": 1.0}
VIDEO_PATH = "inputs/ivideo.h264"

cap = cv2.VideoCapture(VIDEO_PATH)
counter = ObjectCountingAPI(options)

# counter.count_objects_on_video(cap, show=True)
counter.count_objects_crossing_the_virtual_line(cap, line_begin=(100, 170), line_end=(300, 170), show=True)

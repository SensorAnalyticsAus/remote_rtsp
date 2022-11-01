#!/usr/bin/python
import os
import cv2

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"]="rtsp_transport;udp\
	|analyzeduration;9000\
	|reorder_queue_size;2500"
os.environ["OPENCV_FFMPEG_DEBUG"] = "1"
os.environ["OPENCV_LOG_LEVEL"] = "VERBOSE"


x='rtsp://192.168.1.21/onvif1' # sricam url

cap = cv2.VideoCapture(x,cv2.CAP_FFMPEG)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
       print("Frame is empty")
       break;
    else:
       cv2.imshow('VIDEO', frame)
       if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

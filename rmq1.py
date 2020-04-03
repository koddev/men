import pika
import cv2

import json
from datetime import datetime
import base64
import time
import os
import sys


class CamFrameClass:
    def __init__(self, time, image):
        self.time = time
        self.image = image


addressIp='62.244.197.146'
# addressIp='192.168.116.20'

connection = pika.BlockingConnection(pika.ConnectionParameters(addressIp,5550))
channel = connection.channel()
queueName='camlive'
channel.queue_declare(queue=queueName)

# cap = cv2.VideoCapture(1)
# vidPath="/home/cc/video/k1.avi"
cap = cv2.VideoCapture(1)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720);
# cap.set(cv2.CV_CAP_PROP_FPS, 5)

# cap.set(cv2.CAP_PROP_FPS,5)
# stream.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920);
# stream.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080);
# stream.set(cv2.cv.CV_CAP_PROP_FPS, 5)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
averageFps = 0
frameCount=0
startTime=time.time()
# cachePath="~/code/men/cache/aa.jpg"
while True:

    try:
        (g,frame) = cap.read()
        # height, width, depth = frame.shape
        if frame is None:
            break
        if not cap.isOpened():
            break

        # width,height = cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # print(str(width) + " " + str(height))


        # half = cv2.resize(frame, (1280, 720))
        # result, encimg = cv2.imencode('.jpg', frame, encode_param)
        # size = str(sys.getsizeof(data))
        # cv2.imwrite(cachePath,half,encode_param)
        # img = cv2.imread(cachePath)
        # imgSize=os.path.getsize(cachePath)
        # os.remove(cachePath)
        # height, width = img.shape[:2]
        # print(str(width) + " " + str(height) + " " + str(imgSize/1024) + " KB")

        half = cv2.resize(frame, (640, 480))
        result, encimg = cv2.imencode('.jpg', half, encode_param)
        imgSize =  sys.getsizeof(encimg)
        # height, width = half.shape[:2]
        # print(str(width) + " " + str(height) + " " + str(imgSize / 1024) + " KB")

        # imgnp = bytearray(encimg)


        encoded_string = str(base64.b64encode(encimg))
        now = datetime.now().isoformat()
        camClass = CamFrameClass(now, encoded_string)

        jsonStr = json.dumps(camClass.__dict__)
        # print('sending:'+now )
        # + " " + str(width) + "X" + str(height)

        _startTime=time.time()
        channel.basic_publish(exchange='', routing_key=queueName, body=jsonStr)
        frameCount=frameCount+1
        _diffTime=time.time()-_startTime
        # waitTime = 0.01-_diffTime
        # if waitTime>0:
        #     time.sleep(waitTime)

        diffTime = time.time() - startTime

        if diffTime >=5:
            fps=frameCount/5
            print("fps:" + str(fps) + " - " + str(imgSize / 1024))
            startTime = time.time()
            frameCount=0


    except KeyboardInterrupt:
        # print('hata')
        # break the infinite loop
        break





cv2.destroyAllWindows()
connection.close()
exit()




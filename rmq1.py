import pika
import cv2

import json
from datetime import datetime
import base64
import time




class CamFrameClass:
    def __init__(self, time, image):
        self.time = time
        self.image = image


addressIp='62.244.197.146'
#addressIp='192.168.116.20'

connection = pika.BlockingConnection(pika.ConnectionParameters(addressIp,5550))
channel = connection.channel()
channel.queue_declare(queue='cam1')

cap = cv2.VideoCapture(1)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080);
# cap.set(cv2.CAP_PROP_FPS,5)
# stream.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920);
# stream.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080);
# stream.set(cv2.cv.CV_CAP_PROP_FPS, 5)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
averageFps = 0
frameCount=0
startTime=time.time()
while True:

    try:
        (g,frame) = cap.read()
        # height, width, depth = frame.shape
        if frame is None:
            break
        half = cv2.resize(frame, (0, 0), fx=0.6, fy=0.6)
        # half = cv2.resize(frame, (1280, 720))
        result, encimg = cv2.imencode('.jpg', half, encode_param)
        # imgnp = bytearray(encimg)
        if not result:
            continue

        encoded_string = str(base64.b64encode(encimg))
        now = datetime.now().isoformat()
        camClass = CamFrameClass(now, encoded_string)

        jsonStr = json.dumps(camClass.__dict__)
        # print('sending:'+now )
        # + " " + str(width) + "X" + str(height)

        _startTime=time.time()
        channel.basic_publish(exchange='', routing_key='cam1', body=jsonStr)
        frameCount=frameCount+1
        _diffTime=time.time()-_startTime
        waitTime = 0.2-_diffTime
        if waitTime>0:
            time.sleep(waitTime)

        diffTime = time.time() - startTime

        if diffTime >=5:
            fps=frameCount/5
            print("fps:" + str(fps))
            startTime = time.time()
            frameCount=0




    except KeyboardInterrupt:
        # break the infinite loop
        break





cv2.destroyAllWindows()
connection.close()
exit()




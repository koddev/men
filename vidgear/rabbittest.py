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



connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.195.19'))
channel = connection.channel()
channel.queue_declare(queue='camFromBoard')

stream = cv2.VideoCapture("/dev/video1")
stream.set(cv2.CV_CAP_PROP_FRAME_WIDTH, 1920);
stream.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, 1080);
stream.set(cv2.CV_CAP_PROP_FPS, 5)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
while True:

    try:
        (g,frame) = stream.read()

        if frame is None:
            break

        result, encimg = cv2.imencode('.jpg', frame, encode_param)
        imgnp = bytearray(encimg)
        encoded_string = base64.b64encode(encimg)
        now = datetime.now().isoformat()
        cam = CamFrameClass(now, encoded_string)
        #
        jsonStr = json.dumps(cam.__dict__)
        print('sending:'+now)

        channel.basic_publish(exchange='', routing_key='camFromBoard', body=jsonStr)

        time.sleep(0.1)
    except KeyboardInterrupt:
        # break the infinite loop
        break





cv2.destroyAllWindows()
connection.close()
exit()




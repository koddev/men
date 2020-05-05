import cv2
import base64
import sys
import time
import json
from threading import Thread
from guid import GUID


class FaceCapture:  
    def __init__(self, sock):
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.sock = sock
        self.continueStreaming = False


    def send_faces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
        if (len(faces) > 0):
            for (x, y, w, h) in faces:
                roi_color = img[y:y + h, x:x + w]
                result, encimg = cv2.imencode('.jpg', roi_color, self.encode_param)
                encoded_string = base64.b64encode(encimg).decode("utf-8") 
                print("sending face")                           
                Thread(target = self.send_image_thread, args = (encoded_string)).start()
                #self.continueStreaming = False
                #break 


    def send_image_thread(self, *arg):
        sendImage = ''.join(str(v) for v in arg)
        guid = GUID()
        msg = {
            "guid": guid.uuid,
            "image": sendImage,
            "key" : 'Kasif'
        }
        sendMsg = json.dumps(msg)
        self.sock.send(sendMsg.encode())
    
    def startImageStreamThread(self, resolution, fps):
        self.continueStreaming = True
        capture = cv2.VideoCapture(0)
        #fps = int(settings['fps'])
        rate = 1 / fps
        if resolution != '':
            resolution = resolution.split('*')
            capture.set(3, int(resolution[0])),capture.set(4,int(resolution[0]))
        while self.continueStreaming:
            startTime = time.time()
            (g,frame) = capture.read()
            if frame is None:
                continue
            if not capture.isOpened():
                break
            self.send_faces(frame)
            diffTime = rate - (time.time() - startTime)
            if (diffTime > 0):
                time.sleep(diffTime)

        capture.release()
        cv2.destroyAllWindows()

    def startImageStream(self, resolution, fps):
        Thread(target = self.startImageStreamThread, args = (resolution, fps)).start()

    def stopImageStream(self):
        self.continueStreaming = False
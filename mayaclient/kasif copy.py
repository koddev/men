import zipfile
import json
from datetime import datetime
import base64
import time
import os
import sys
import queue
import threading
import psutil
from persistqueue import Queue
import queue
import os
import time
import pygame.camera
import pygame.image
from PIL import Image
import cv2
import guid
import pika
import socket
from guid import GUID

# from Tensor import TensorFaceDetector
# import numpy as np

# from utils import label_map_util
# from utils import visualization_utils_color as vis_util

# tcpPort = 5551
# sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IsConnected=False

 
# max_que_size=200
 
# queueFrame=queue.LifoQueue(max_que_size)
# is_exit=False
# pygame.camera.init()
# cameras = pygame.camera.list_cameras()  


class KasifClass(object):
    def __init__(self):
        self.IsConnected=False
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpPort = 5551
        self.serverIP='62.244.197.146'
        self.max_que_size=50
        self.queueFrame=queue.LifoQueue(self.max_que_size)
        self.is_exit=False
        pygame.camera.init()
        self.cameras = pygame.camera.list_cameras()
        # self.t1=TensorFaceDetector()
        




    def killCaptureProcess(self):
        for camName in self.cameras:
            stream = os.popen('fuser ' + camName)
            output=stream.read().strip().split()
            while len(output)>0:
                for i in output:
                    os.kill(int(i),9)
                    print('kill')
                    time.sleep(0.05)
                stream = os.popen('fuser ' + camName)
                output=stream.read().strip().split()



    def capture(self,*args):
          
        self.killCaptureProcess()
        # while not self.cameras[0]:
        #     time.sleep(0.1)
        #     self.cameras = pygame.camera.list_cameras()
        #     print('camera waittt')

        webcam = pygame.camera.Camera(self.cameras[0])
        webcam.start()
        # img = webcam.get_image()
        # WIDTH = img.get_width()
        # HEIGHT = img.get_height()
    
    
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        _fpsStartTime=time.time()
        _frameCount=0
    
    
        # print("Width: %d, Height: %d, FPS: %d" % (cap.get(3), cap.get(4), cap.get(5)))
        while not self.is_exit:        
            # time.sleep(0.1)
            if  psutil.virtual_memory()[2]>90 or self.queueFrame.qsize()>self.max_que_size: #queueFrame.qsize()>max_que_size: #queueFrame.full() or
                # print('queue/memory is full')
                self.queueFrame.get()
                # queueFrame.task_done()
                # sys.exit()
                
        
            img= webcam.get_image()
            # os.chdir("/home/kom/Pictures")
            # pygame.image.save(img,"/home/kom/asd.jpg")
            # pil_string_image = pygame.image.tostring(img,"RGBA",False)
            # im = Image.frombytes("RGBA",(1920,1080),pil_string_image)
            # img=pygame.transform.rotate(img,90)
            # pygame.image.save(img,"/home/kom/asd.jpg")


            frame = pygame.surfarray.array3d(img)
            frame = cv2.transpose(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


            # frame640 = cv2.resize(frame,(1024,576))            
            # encimg = cv2.imwrite('aa.jpg', frame640, encode_param) 
            result, encimg = cv2.imencode('.jpg', frame, encode_param) 
            
    
    
            self.queueFrame.put(encimg)
            _frameCount+=_frameCount
    
             
            


    def connect(self):
        try:     
            # sock.close() 
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.serverIP,self.tcpPort))  
            self.IsConnected=True
        except Exception as e:
            # self.sock.close
            print(e)
    

    def sendImageAsync(self,*img):

        encoded_string = base64.b64encode(img[0]).decode("utf-8")
        imgSize =  sys.getsizeof(encoded_string)
        guid = GUID()

        msg = {
            "guid": guid.uuid,
            "image": encoded_string,
            "key" : "Kasif"
        }

        # print(encoded_string)
        sendMsg = json.dumps(msg)
        try:
            self.sock.send(sendMsg.encode())
            print(str(imgSize) + ' - ' + str(self.queueFrame.qsize()) + ' memory % used:', psutil.virtual_memory()[2])
        except Exception as ex:
            self.IsConnected=False
            print(ex)


    def FaceDetect(self,*img):
        frame = cv2.cvtColor(img[0], cv2.COLOR_RGB2BGR)
        try:
            (boxes, scores, classes, num_detections) = self.t1.run(frame)
            print(boxes, scores, classes, num_detections)
        except Exception as e:
            print(e)



    def start(self):
        p = []

        try:
            self.connect()
            print('start')

            p.append(threading.Thread(target=self.capture, args=(1,)))
            p[0].daemon=True
            p[0].start()

            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            #     s.connect((serverIP,tcpPort))    

            while True:
                if self.queueFrame.empty():
                    time.sleep(0.1)
                    continue
                while not self.IsConnected:
                    time.sleep(3)
                    print('retry connect')
                    self.connect()                

 
                
                frame=self.queueFrame.get()
                # frameResize=cv2.resize(frame,(960,540))
                # self.FaceDetect(frameResize)

                print('ok')
                # self.sendImageAsync(frame)
                # sendThread=threading.Thread(target=self.sendImageAsync, args=(frame,))
                # sendThread.daemon=True
                # sendThread.start()


                
                # print(imgSize)
                # print(queueFrame.qsize())
                # print(psutil.virtual_memory())  # physical memory usage
                

        except Exception as e:
            print(e)
            # is_exit=True


        p[0].join()


if __name__ == '__main__':
    kasif=KasifClass()
    kasif.start()
    

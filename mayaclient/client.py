import cv2
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

addressIp='62.244.197.146'
# addressIp='192.168.116.20'

# connection = pika.BlockingConnection(pika.ConnectionParameters(addressIp,5550))
# channel = connection.channel()
# queueName='camlivetest'
# channel.queue_declare(queue=queueName)

max_que_size=100
# queueFrame=Queue("testimagecache") 
queueFrame=queue.LifoQueue(100)
is_exit=False



class CamFrameClass:
    def __init__(self, time, image):
        self.time = time
        self.image = image





def capture(*args):
        
        cap = cv2.VideoCapture(0)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        _fpsStartTime=time.time()
        _frameCount=0


        # print("Width: %d, Height: %d, FPS: %d" % (cap.get(3), cap.get(4), cap.get(5)))
        while True:
            
            time.sleep(0.01)
            if  psutil.virtual_memory()[2]>90 or queueFrame.qsize()>max_que_size: #queueFrame.qsize()>max_que_size: #queueFrame.full() or
                print('queue/memory is full')
                queueFrame.get()
                # queueFrame.task_done()
                # sys.exit()
        

            ret, frame = cap.read()

            if ret != True:
                time.sleep(0.1)
                continue

            result, encimg = cv2.imencode('.jpg', frame, encode_param)    
            queueFrame.put(encimg)
            _frameCount+=_frameCount

            if is_exit:
                break

            # _diff=time.time()-_fpsStartTime
            # if _diff>5:
            #     _fps=_frameCount/_diff/5
            #     print('FPSSSSS   :' + str(_fps))
            #     _frameCount=0
            #     _fpsStartTime=time.time()
             
        cap.release()
        cv2.destroyAllWindows()








if __name__ == '__main__':
    p = []
    try:

        print('start')
        

        p.append(threading.Thread(target=capture, args=(1,)))
        p[0].daemon=True
        p[0].start()

        while True:
            if queueFrame.empty():
                time.sleep(0.1)
            frame=queueFrame.get()

            imgSize =  sys.getsizeof(frame)
            # print(imgSize)
            # print(queueFrame.qsize())
            # print(psutil.virtual_memory())  # physical memory usage
            print('memory % used:', psutil.virtual_memory()[2])
            time.sleep(0.1)
            

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

             
    except :
        print('keyboard interrupt MAi')
        is_exit=True
        
    
    p[0].join()

  

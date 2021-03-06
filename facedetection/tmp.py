from Tensor import TensorFaceDetector
import cv2
import numpy as np

import asyncio
import concurrent.futures
from PIL import Image
from matplotlib.image import imread
import os
import time

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


path_model = './model/frozen_inference_graph_face.pb'
path_label = './protos/face_label_map.pbtxt'
num_classes = 2



# cap = cv2.VideoCapture("D:/cc/code/Python/video/istiklal1.mp4")


# cap = cv2.VideoCapture(0)


# img1=Image.open('./tmpfaces/1.jpg')
# img2=Image.open('./tmpfaces/2.jpg')
# img22=np.asarray(img1)
img11=imread('./tmpfaces/1.jpg')
img22=imread('./tmpfaces/22.jpg')

imgs=np.asarray((img11,img22))
t1 = TensorFaceDetector()
# t2 = TensorFaceDetector()
# fun=(t1,t2)



# res1=t1(img11)

def hold(n):
    print(f'Running task number {n} - {os.getpid()}')
    time.sleep(n)
    return n

def imgasync(img):
    print(f'ASS: {os.getpid()}')
    return t1.run(img)


async def parcala():

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures=[]

        for i in range(500):
            futures.append(executor.submit(imgasync, img22))


        # futures.append(executor.submit(TensorFaceDetector().run,img11))
        # futures.append(executor.submit(t1.run, img22))
        # futures = {executor.submit(hold, i) for i in range(5)}
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            # print('complete' + str(os.getpid()))





if __name__ == '__main__':
    _start = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(parcala())
    loop.run_until_complete(future)
    print(f"Execution time: { time.time() - _start } - {os.getpid()}")
    loop.close()



# tDetectors = []
# if not tDetectors:
#     for item in range(2):
#         tDetectors.append(TensorFaceDetector())
#     # for item in tDetectors:
#     #     item=foo
#
#
# print(tDetectors)
#
#
# for item in tDetectors:
#     print(id(item))




from TensorLite import TensorLiteDetector
from PIL import Image
import numpy as np
import cv2

img=Image.open("/home/kom/code/men/test/images/3.jpg")
a=np.asarray(img)
 


detector = TensorLiteDetector()
objs = detector.detectFace(a)
cv2_im = detector.append_objs_to_img(a, objs)


cv2.imwrite('/home/kom/Pictures/3.jpg',cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB))

print('')


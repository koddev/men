import cv2
import numpy as np
from goprocam import GoProCamera
from goprocam import constants


vidcap = cv2.VideoCapture("udp://127.0.0.1:10000")
success,image = vidcap.read()
success = True
while success:
  cv2.imwrite("frame.jpg", image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
import cv2
import time


cap=cv2.VideoCapture(2)

success,frame = cap.read()
while success:
    cv2.imshow("gopro",frame)
    success, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

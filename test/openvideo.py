import cv2
import os
import time
import pygame.camera
import pygame.image
import sys
import time

pygame.camera.init()
cameras = pygame.camera.list_cameras()
 


def killCaptureProcess():
    for camName in cameras:
        stream = os.popen('fuser ' + camName)
        output=stream.read().strip().split()
        while len(output)>0:
            for i in output:
                os.kill(int(i),9)
                print('kill')
                time.sleep(0.05)
            stream = os.popen('fuser ' + camName)
            output=stream.read().strip().split()



    

def getVideoCapture():
    killCaptureProcess()    
    for c in cameras:
        cap=cv2.VideoCapture(c)
        ret, frame = cap.read()
        if ret == True:
            return cap
        else:
            cap.release()





cap=getVideoCapture()
while(True):
    # Capture frame-by-frame
    
    ret, frame = cap.read()
    if ret != True:
        print('starttt')
        continue

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
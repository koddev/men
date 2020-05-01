import cv2
import os


stream = os.popen('fuser /dev/video0')
output=stream.read().strip().split()
for i in output:
    os.kill(int(i),9)

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    print('starttt')
    ret, frame = cap.read()
    if ret != True:
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
from vidgear.gears import CamGear
import cv2

# open any valid video stream(for e.g `myvideo.avi` file)

stream = CamGear(source='https://youtu.be/u5eHGKW0KkE', y_tube =True).start()
# loop
while True:
    # read frames
    frame = stream.read()

    # check if frame is None
    if frame is None: break

    # do something with frame here

    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for 'q' key-press
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()
# safely close video stream.
stream.stop()
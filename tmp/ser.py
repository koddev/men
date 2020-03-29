from vidgear.gears import VideoGear
from vidgear.gears import NetGear
from vidgear.gears import WriteGear
import cv2

from time import sleep

#writer = WriteGear(output_filename = 'Output.mp4') #Define writer

vid_path="/mnt/sd/istiklal.mp4"
# vid_path="/home/cc/PycharmProjects/assets/istiklal1.mp4"
# stream = VideoGear(source=vid_path).start()  # Open any video stream
stream = cv2.VideoCapture(vid_path)  # Open any video stream

options = {'flag': 0, 'copy': False, 'track': False}

# change following IP address '192.168.x.xxx' with client's IP address
server = NetGear(address='192.168.1.25', port='5454', protocol='tcp', pattern=0, receive_mode=False, logging=True,
                 **options)  # Define netgear server at your system IP address.

# infinite loop until [Ctrl+C] is pressed
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
while True:


    try:
        frame = stream.read()
        # read frames



        # check if frame is None
        if frame is None:
            # if True break the infinite loop
            break

        # do something with frame here

        # send frame to server

        # sleep(1/90)

        result, encimg = cv2.imencode('.jpg', frame, encode_param)
        server.send(encimg)


    except KeyboardInterrupt:
        # break the infinite loop
        break

# safely close video stream
stream.stop()
# safely close server
server.close()
exit()

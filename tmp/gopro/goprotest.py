from goprocam import GoProCamera
from goprocam import constants
import cv2
import time

gopro = GoProCamera.GoPro()
# gopro.video_settings(res='1080p', fps='30')
# gopro.gpControlSet(constants.Stream.WINDOW_SIZE, constants.Stream.WindowSize.R240)

# gopro.streamSettings(constants.Stream.BitRate.B2_5Mbps,constants.Stream.WindowSize.R720_1by2Subsample)
gopro.mode("2","0")
gopro.mode("2","0")
gopro.mode("2","0")
gopro.mode("2","0")

# gopro.mode(constants.Mode.PhotoMode,constants.Mode.SubMode.MultiShot.Burst)
# gopro.take_photo()
while True:
    gopro.shutter("1")
    ready = int(gopro.getStatus(constants.Status.Status,
                               constants.Status.STATUS.IsBusy))
    while ready == 1:
        ready = int(gopro.getStatus(constants.Status.Status,
                                   constants.Status.STATUS.IsBusy))
    time.sleep(0.5)
    print(gopro.getMedia())

# gopro.stream("udp://127.0.0.1:10000")





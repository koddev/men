from goprocam import GoProCamera
from goprocam import constants
import cv2

gopro = GoProCamera.GoPro()
# gopro.video_settings(res='1080p', fps='30')
# gopro.gpControlSet(constants.Stream.WINDOW_SIZE, constants.Stream.WindowSize.R240)

# gopro.streamSettings(constants.Stream.BitRate.B2_5Mbps,constants.Stream.WindowSize.R720_1by2Subsample)
gopro.mode(constants.Mode.VideoMode,constants.Mode.)
gopro.stream("udp://127.0.0.1:10000")





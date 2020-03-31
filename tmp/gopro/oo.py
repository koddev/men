from goprocam import GoProCamera
from goprocam import constants
import cv2
import time





gopro = GoProCamera.GoPro()
gopro.streamSettings("2400000", "6")
# gopro.livestream("stop")
gopro.stream("udp://127.0.0.1:10000")
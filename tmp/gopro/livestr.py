from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro()
# gpCam.streamSettings(2400000,9)

gpCam.livestream("start")
gpCam.streamSettings(2400000,9)

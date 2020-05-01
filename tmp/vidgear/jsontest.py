import json
import time
from datetime import datetime

now = datetime.now().isoformat()




class CamFrameClass:
    def __init__(self, time, image):
        self.time = time
        self.image = image


cam = CamFrameClass(now,"asdfasdfasdf")

jsonStr = json.dumps(cam.__dict__)
print(jsonStr)



import cv2
import base64
import sys
import json
from faceCapture import FaceCapture
from settings import Settings


class Command:
    def __init__(self, sock):
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.sock = sock
        self.settings = Settings()
        self.faceCapture = FaceCapture(sock)


    def change_resolution(self, w, h):    
        capture = cv2.VideoCapture(0)
        capture.set(3, w),capture.set(4,h)
        new_size = int(capture.get(3)), int(capture.get(4))

        capture.release()
        cv2.destroyAllWindows()
        return new_size

    def get_resolution_list(self):
        resolution_list = [(160, 120),(320,480),(640,480),(960,680),(1280,720),(1920,1080)]
        supported_resolutions = []
        for resolution in resolution_list:
            new_resolution = self.change_resolution(resolution[0], resolution[1])
            try:
                supported_resolutions.index(new_resolution)
            except:
                supported_resolutions.append(new_resolution)
                
        return supported_resolutions

    def get_sample_image(self, resolution):
        capture = cv2.VideoCapture(0)
        if resolution != '':
            resolution = resolution.split('*')
            capture.set(3, int(resolution[0])),capture.set(4,int(resolution[0]))

        (g,frame) = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # height, width, depth = frame.shape
        result, encimg = cv2.imencode('.jpg', frame, self.encode_param)
        #imgSize =  sys.getsizeof(encimg)
        imgStr = str(base64.b64encode(encimg))
        capture.release()
        cv2.destroyAllWindows()

        return imgStr

    def parse_command(self, commandStr):
        cmd = json.loads(commandStr)
        print(cmd)
        if 'cmd' in cmd.keys():
            commands = cmd['cmd'].split(':')
            if commands[0] == '#CMD':
                if commands[1] == 'RESOLUTION':
                    res_list = self.get_resolution_list()
                    msg = {
                        "requestId": cmd["requestId"],
                        "response": res_list
                    }
                    response = json.dumps(msg)
                    self.sock.send(response.encode())

                elif commands[1] == 'SAMPLEIMAGE':
                    sample_image = self.get_sample_image(self.settings.settings["resolution"])
                    msg = {
                        "requestId": cmd["requestId"],
                        "response": sample_image
                    }
                    response = json.dumps(msg)
                    self.sock.send(response.encode())

                elif commands[1] == 'CHANGEFPS':
                    self.settings.change_setting('fps', int(commands[2]))
                    msg = {
                        "requestId": cmd["requestId"],
                        "response": "FPS " + str(commands[2]) + " olarak ayarlandı"
                    }
                    response = json.dumps(msg)
                    self.sock.send(response.encode())

                elif commands[1] == 'CHANGERESOLUTION':
                    self.settings.change_setting('resolution', commands[2])
                    msg = {
                        "requestId": cmd["requestId"],
                        "response": "Çözünürlük " + commands[2] + " olarak ayarlandı"
                    }
                    response = json.dumps(msg)
                    self.sock.send(response.encode())

                elif commands[1] == 'GETSETTINGS':
                    msg = {
                        "requestId": cmd["requestId"],
                        "response": self.settings.settings
                    }
                    response = json.dumps(msg)
                    self.sock.send(response.encode())

                elif commands[1] == 'STREAMSTART': 
                    msg = {
                        "requestId": cmd["requestId"],
                        "response": "Stream Başladı"
                    }
                    self.faceCapture.startImageStream(self.settings.settings["resolution"], self.settings.settings["fps"])
                    response = json.dumps(msg)
                    self.sock.send(response.encode())
                elif commands[1] == 'STREAMSTOP':
                    self.faceCapture.stopImageStream()
                    msg = {
                        "requestId": cmd["requestId"],
                        "response": "Stream Durduruldu"
                    }
                    response = json.dumps(msg)
                    self.sock.send(response.encode())
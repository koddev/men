import pygame.camera
import pygame.image
import sys
import os

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


pygame.camera.init()
cameras = pygame.camera.list_cameras()
killCaptureProcess()



print ("Using camera %s ..." % cameras[0])
webcam = pygame.camera.Camera(cameras[0])

webcam.start()
# grab first frame
img = webcam.get_image()
WIDTH = img.get_width()
HEIGHT = img.get_height()
screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption("pyGame Camera View")
while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()
    # draw frame
    screen.blit(img, (0,0))
    pygame.display.flip()
    # grab next frame    
    img = webcam.get_image()
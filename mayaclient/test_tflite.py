
import tensorflow as tf
import numpy as np
import collections
from collections import deque
import io
import os
import pygame.camera
import pygame
from pygame.locals import *
import re
import sys
import time


Object = collections.namedtuple('Object', ['id', 'score', 'bbox'])


class BBox(collections.namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])):
    """Bounding box.
    Represents a rectangle which sides are either vertical or horizontal, parallel
    to the x or y axis.
    """
    __slots__ = ()

def get_output(interpreter, score_threshold, top_k, image_scale=1.0):
    """Returns list of detected objects."""
    boxes = output_tensor(interpreter, 0)
    class_ids = output_tensor(interpreter, 1)
    scores = output_tensor(interpreter, 2)

    def make(i):
        ymin, xmin, ymax, xmax = boxes[i]
        return Object(
            id=int(class_ids[i]),
            score=scores[i],
            bbox=BBox(xmin=np.maximum(0.0, xmin),
                      ymin=np.maximum(0.0, ymin),
                      xmax=np.minimum(1.0, xmax),
                      ymax=np.minimum(1.0, ymax)))

    return [make(i) for i in range(top_k) if scores[i] >= score_threshold]



def input_image_size(interpreter):
    """Returns input image size as (width, height, channels) tuple."""
    _, height, width, channels = interpreter.get_input_details()[0]['shape']
    return width, height, channels

def input_tensor(interpreter):
    """Returns input tensor view as numpy array of shape (height, width, 3)."""
    tensor_index = interpreter.get_input_details()[0]['index']
    return interpreter.tensor(tensor_index)()[0]

def output_tensor(interpreter, i):
    """Returns dequantized output tensor if quantized before."""
    output_details = interpreter.get_output_details()[i]
    output_data = np.squeeze(interpreter.tensor(output_details['index'])())
    if 'quantization' not in output_details:
        return output_data
    scale, zero_point = output_details['quantization']
    if scale == 0:
        return output_data - zero_point
    return scale * (output_data - zero_point)



cam_w, cam_h = 1920, 1080
model = "/home/kom/code/men/mayaclient/models/mobilenet_ssd_v2_face_quant_postprocess.tflite"

interpreter = tf.lite.Interpreter(model_path=model)
interpreter.allocate_tensors()

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

pygame.camera.init()
camlist = pygame.camera.list_cameras()

w, h, _ = input_image_size(interpreter)
camera = pygame.camera.Camera(camlist[-1], (cam_w, cam_h))
# try:
#     display = pygame.display.set_mode((cam_w, cam_h), 0)
# except pygame.error as e:
#     sys.stderr.write("\nERROR: Unable to open a display window. Make sure a monitor is attached and that "
#         "the DISPLAY environment variable is set. Example: \n"
#         ">export DISPLAY=\":0\" \n")
#     raise e

red = pygame.Color(255, 0, 0)
camera.start()


try:
    last_time = time.monotonic()
    while True:
        mysurface = camera.get_image()
        imagen = pygame.transform.scale(mysurface, (w, h))
        input = np.frombuffer(imagen.get_buffer(), dtype=np.uint8)
        start_time = time.monotonic()
        input_tensor(interpreter)[:,:] = np.reshape(input, (input_image_size(interpreter)))
        interpreter.invoke()
        results = get_output(interpreter, score_threshold=0.5, top_k=5)
        stop_time = time.monotonic()
        inference_ms = (stop_time - start_time)*1000.0
        fps_ms = 1.0 / (stop_time - last_time)
        last_time = stop_time
        annotate_text = 'Inference: {:5.2f}ms FPS: {:3.1f}'.format(inference_ms, fps_ms)
        for result in results:
            x0, y0, x1, y1 = list(result.bbox)
            rect = pygame.Rect(x0 * cam_w, y0 * cam_h, (x1 - x0) * cam_w, (y1 - y0) * cam_h)
            pygame.draw.rect(mysurface, red, rect, 1)
        #     label = '{:.0f}% {}'.format(100*result.score, labels.get(result.id, result.id))
        #     text = font.render(label, True, red)
        #     print(label, ' ', end='')
        #     mysurface.blit(text, (x0 * cam_w , y0 * cam_h))
        # text = font.render(annotate_text, True, red)
        # print(annotate_text)
        # mysurface.blit(text, (0, 0))
        # display.blit(mysurface, (0, 0))
        # pygame.display.flip()
finally:
    camera.stop()


print('')


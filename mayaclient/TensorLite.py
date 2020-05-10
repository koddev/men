 
from PIL import Image
import collections

import cv2
import numpy as np
import os
from PIL import Image

import tensorflow as tf

Object = collections.namedtuple('Object', ['id', 'score', 'bbox'])
 
class BBox(collections.namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])):
    """Bounding box.
    Represents a rectangle which sides are either vertical or horizontal, parallel
    to the x or y axis.
    """
    __slots__ = ()

class TensorLiteDetector(object):
    def __init__(self):
        self.cam_w, self.cam_h = 1920, 1080
        self.model = "/home/kom/code/men/mayaclient/models/mobilenet_ssd_v2_face_quant_postprocess.tflite"
        self.interpreter = tf.lite.Interpreter(model_path=self.model)
        self.interpreter.allocate_tensors()
        self.w, self.h, _ = self.input_image_size()

    def detectFace(self,img):
        cv2_im = img
        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        pil_im= Image.fromarray(cv2_im_rgb)
        self.set_input(pil_im)
        self.interpreter.invoke()
        objs = self.get_output(self.interpreter, score_threshold=0.5, top_k=15)
        return objs
        
        # last_time = time.monotonic()
        # mysurface = img[0]
        # imagen = pygame.transform.scale(mysurface, (self.w, self.h))
        # input = np.frombuffer(imagen.get_buffer(), dtype=np.uint8)
        # start_time = time.monotonic()
        # inputtensor=np.reshape(input, (self.input_image_size()))
        # self.input_tensor()[:,:] = inputtensor
        # self.interpreter.invoke()
        # results = self.get_output(self.interpreter, score_threshold=0.5, top_k=15)
        # stop_time = time.monotonic()
        # inference_ms = (stop_time - start_time)*1000.0
        # fps_ms = 1.0 / (stop_time - last_time)
        # last_time = stop_time
        # annotate_text = 'Inference: {:5.2f}ms FPS: {:3.1f}'.format(inference_ms, fps_ms)
        # print(annotate_text)
        # return results

    def get_output(self,interpreter, score_threshold, top_k, image_scale=1.0):
        """Returns list of detected objects."""
        boxes = self.output_tensor(0)
        class_ids = self.output_tensor(1)
        scores = self.output_tensor(2)

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


    def set_input(self,image, resample=Image.NEAREST):
        """Copies data to input tensor."""
        image = image.resize((self.input_image_size()[0:2]), resample)
        self.input_tensor()[:, :] = image

    def input_image_size(self):
        """Returns input image size as (width, height, channels) tuple."""
        _, height, width, channels = self.interpreter.get_input_details()[0]['shape']
        return width, height, channels

    def input_tensor(self):
        """Returns input tensor view as numpy array of shape (height, width, 3)."""
        tensor_index = self.interpreter.get_input_details()[0]['index']
        return self.interpreter.tensor(tensor_index)()[0]

    def output_tensor(self, i):
        """Returns dequantized output tensor if quantized before."""
        output_details = self.interpreter.get_output_details()[i]
        output_data = np.squeeze(self.interpreter.tensor(output_details['index'])())
        if 'quantization' not in output_details:
            return output_data
        scale, zero_point = output_details['quantization']
        if scale == 0:
            return output_data - zero_point
        return scale * (output_data - zero_point)
    

    def append_objs_to_img(self,cv2_im, objs):
        height, width, channels = cv2_im.shape
        for obj in objs:
            x0, y0, x1, y1 = list(obj.bbox)
            x0, y0, x1, y1 = int(x0*width), int(y0*height), int(x1*width), int(y1*height)
            percent = int(100 * obj.score)
            # label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

            cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
            # cv2_im = cv2.putText(cv2_im, '', (x0, y0+30),
            #                      cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        return cv2_im

    
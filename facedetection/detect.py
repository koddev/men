from Tensor import TensorFaceDetector
import cv2
import numpy as np
from utils import label_map_util
from utils import visualization_utils_color as vis_util
import asyncio
import concurrent.futures

path_model = './model/frozen_inference_graph_face.pb'
path_label = './protos/face_label_map.pbtxt'
num_classes = 2

label_map = label_map_util.load_labelmap(path_label)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=num_classes,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# cap = cv2.VideoCapture("D:/cc/code/Python/video/istiklal1.mp4")
cap = cv2.VideoCapture('C:/Code/PythonDocs/video/kizilayara.mp4')


# cap = cv2.VideoCapture(0)

tDetectors = []

async def detectAsync(images):
    if not tDetectors:
        for item in range(5):
            tDetectors.append(TensorFaceDetector())

async def startDetect():

    while True:
        ret, image = cap.read()
        if ret == 0:
            break
        [h, w] = image.shape[:2]
        print(h, w)





async def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(hold, i) for i in range(5)}
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            print(str(data) + " " + str(os.getpid()))


if __name__ == "__main__":
    import sys

    tDetector = TensorFaceDetector()
    while True:
        ret, image = cap.read()
        if ret == 0:
            break
        [h, w] = image.shape[:2]
        print(h, w)
        # image = cv2.flip(image, 1)

        (boxes, scores, classes, num_detections) = tDetector.run(image)

        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=4)

        cv2.imshow("tensorflow based (%d, %d)" % (w, h), image)

        k = cv2.waitKey(1) & 0xff
        if k == ord('q') or k == 27:
            break

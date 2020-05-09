import face_recognition
from PIL import Image

image = face_recognition.load_image_file("/home/kom/code/men/mayaclient/faces.png")
face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()

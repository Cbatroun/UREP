from imageai.Detection import ObjectDetection
import os
import cv2
import timeit

#constants
dirpath = os.getcwd()

detector = ObjectDetection()
#print(dirpath)
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(dirpath, '..', "model\\yolo.h5"))
detector.loadModel("fast")
custom = detector.CustomObjects(car=True)

camera = cv2.VideoCapture(os.path.join(dirpath, "videoplayback.mp4"))
#camera = cv2.VideoCapture(0)
tracker=0
while True:
    #tracker=tracker +1
    ret, frame = camera.read()
    frame_proc,detection = detector.detectCustomObjectsFromImage(input_image=frame, custom_objects=custom, input_type="array", output_type="array")

    cv2.imshow("AI stream", cv2.resize(frame_proc, (800,600)))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break



from imageai.Detection import ObjectDetection
from multiprocessing import Process, Queue
import os
import cv2

#constants
dirpath = os.getcwd()

detector = ObjectDetection()
#print(dirpath)
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(dirpath, '..', "model\\yolo.h5"))
detector.loadModel("fast")
custom = detector.CustomObjects(car=True)

camera = cv2.VideoCapture(os.path.join(dirpath, "parkingvideo.mp4"))
#camera = cv2.VideoCapture(0)
tracker = 0

running = 1
curr_frame = 0


def detect(q):
    while True:
        #tracker=tracker +1
        ret, frame = camera.read()
        frame_proc,detection = detector.detectCustomObjectsFromImage(input_image=frame, custom_objects=custom, input_type="array", output_type="array")
        curr_frame = curr_frame + 1
        q.put(detection)
        
        cv2.imshow("AI stream", cv2.resize(frame_proc, (800, 600)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            running = 0
            break


if __name__ == '__main__':
    curr_frame = 0
    q = Queue()
    p = Process(target=detect, args=(q, ))
    p.start()
    # p.join()
    while running == 1:
        print(q.get())
        for x in q.get():
            if x['percentage_probability'] > 90:
                print(x)

import os
import cv2
import time
#constants
dirpath = os.getcwd()
frame_dir = os.path.join(dirpath,"Frames", "frame.png")
print(frame_dir)
detector = ObjectDetection()
#print(dirpath)
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(dirpath, '..', "model\\yolo.h5"))
detector.loadModel()
camera = cv2.VideoCapture(os.path.join(dirpath, "traffic-mini.mp4"))
time.perf_counter()
while True:
    ret, frame = camera.read()
    cv2.imwrite(frame_dir, frame)
    detection = detector.detectObjectsFromImage(input_image=frame_dir, output_image_path=frame_dir)
    #frame_proc = cv2.imread(frame_dir)
    #cv2.imshow("AI stream", cv2.resize(frame_proc, (800,600)))
    #if cv2.waitKey(25) & 0xFF == ord('q'):
        #cv2.destroyAllWindows()
        #break

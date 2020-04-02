from imageai.Detection import VideoObjectDetection
import os

detector = VideoObjectDetection()
dirpath = os.getcwd()
print(dirpath)
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(dirpath, '..', "model\\yolo.h5"))
detector.loadModel()
detection = detector.deromVideo(input_file_path= os.path.join(dirpath, "traffic-mini.mp4"), output_file_path=os.path.join(dirpath, "traffic_mini_detected_1.mp4"),log_progress=true)tectObjectsF
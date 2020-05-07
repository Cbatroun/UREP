from imageai.Detection import ObjectDetection
from multiprocessing import Process, Queue
import os
import cv2

# constants
dirpath = os.getcwd()

detector = ObjectDetection()
# print(dirpath)
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(dirpath, '..', "model\\yolo.h5"))
detector.loadModel("fast")
custom = detector.CustomObjects(car=True)

camera = cv2.VideoCapture(os.path.join(dirpath, "parkingvidoe01.mp4"))
# camera = cv2.VideoCapture(0)
tracker = 0

running = 1
curr_frame = 0

# def dist(xr, ys):
#     return math.sqrt(sum([(a - b) ** 2 for a, b in zip(xr, ys)]))


def detect(q, f):
    initial = 0
    c = 0
    while True:
        if initial == 0:
            # tracker=tracker +1
            ret, frame = camera.read()

            frame_proc, detection = detector.detectCustomObjectsFromImage(input_image=frame, custom_objects=custom,
                                                                          input_type="array", output_type="array")
            q.put(detection)

            cv2.imshow("AI stream", cv2.resize(frame_proc, (800, 600)))
            # initial = 1
            c += 1
            f.put(c)
        if cv2.waitKey(25) & 0xFF == ord('l'):
            # tracker=tracker +1
            ret, frame = camera.read()
            frame_proc, detection = detector.detectCustomObjectsFromImage(input_image=frame, custom_objects=custom,
                                                                          input_type="array", output_type="array")
            q.put(detection)

            cv2.imshow("AI stream", cv2.resize(frame_proc, (800, 600)))
            c += 1
            f.put(c)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            running = 0
            break


class Point:
    def __init__(self, x, y, p_id):
        self.x = x
        self.y = y
        self.p_id = p_id + 1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "Point(id=" + str(self.p_id) + ",x=" + str(self.x) + ",y=" + str(self.y) + ")"


frames = {
    '0': {
        'points': [Point(0, 0, -1)]
    }
}

print("0,", *frames["0"]['points'])

if __name__ == '__main__':
    q = Queue()
    f = Queue()
    p = Process(target=detect, args=(q, f))
    p.start()
    # p.join()

    while running == 1:
        cf = str(f.get())
        for g in q.get():
            if g['percentage_probability'] > 81:
                # print(x)
                xc = (g['box_points'][0] + g['box_points'][2]) / 2
                yc = (g['box_points'][1] + g['box_points'][3]) / 2
                # print("center x: ", xc.__str__(), " -  y: " + yc.__str__())
                if cf in frames.keys():
                    p = frames[cf]['points']
                    p.append(Point(xc, yc, p[p.__len__() - 1].p_id))
                else:
                    frames[cf] = {
                        'points': [Point(xc, yc, -1)]
                    }

        if frames.__len__() > 3:
            rf = str(int(cf) - 3)
            frames.pop(rf)

        print(str(cf) + ",", *frames[str(cf)]['points'])

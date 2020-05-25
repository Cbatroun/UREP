from imageai.Detection import ObjectDetection
from multiprocessing import Process, Queue
import os
import cv2
import math

# constants
dirpath = os.getcwd()

detector = ObjectDetection()
# print(dirpath)
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(dirpath, '..', "model\\yolo.h5"))
detector.loadModel("fast")
custom = detector.CustomObjects(car=True)

camera = cv2.VideoCapture(os.path.join(dirpath, "Aivideo.mp4"))
# camera = cv2.VideoCapture(0)
tracker = 0

running = 1
curr_frame = 0


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

            cv2.imshow("AI stream", frame_proc)
            #initial = 1
            c += 1
            f.put(c)
        if cv2.waitKey(25) & 0xFF == ord('l'):
            skip = 0
            while skip < 40:
                # tracker=tracker +1
                ret, frame = camera.read()
                frame_proc, detection = detector.detectCustomObjectsFromImage(input_image=frame, custom_objects=custom,
                                                                          input_type="array", output_type="array")
                q.put(detection)

                cv2.imshow("AI stream", frame_proc)
                c += 1
                skip += 1
                f.put(c)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            running = 0
            break


def distance(a1, b1, a2, b2):
    return math.sqrt((a2 - a1)**2 + (b2 - b1)**2)


class Point:
    def __init__(self, xp, yp, c, here):
        self.x = xp
        self.y = yp
        self.timer = 0
        self.here = here
        self.startx = xp
        self.starty = yp
        self.parked = False
        self.moved =False
        self.c = c
        # self.nextTo = []

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "Point(percent=" + str(self.c) + ",x=" + str(self.x) + ",y=" + str(self.y) \
               + ", timer=" + str(self.timer) + ", heretime=" + str(self.here)+ ", parked=" + str(self.parked)\
               + ",startx=" + str(self.startx) + ",starty=" + str(self.starty) + ",moved=" + str(self.moved)+")"


centroids = {
    '0': {
        'points': [Point(0, 0, 0, 0)]
    }
}

print("0,", *centroids["0"]['points'])

if __name__ == '__main__':
    q = Queue()
    f = Queue()
    p = Process(target=detect, args=(q, f))
    p.start()
    # p.join()

    while running == 1:
        cf = str(f.get())
        for g in q.get():
            percentage = g['percentage_probability']
            x1 = g['box_points'][0]
            y1 = g['box_points'][1]
            x2 = g['box_points'][2]
            y2 = g['box_points'][3]
            if percentage > 70:
                # print(x)
                xc = (x1 + x2) / 2
                yc = (y1 + y2) / 2
                # print("center x: ", xc.__str__(), " -  y: " + yc.__str__())
                if cf in centroids.keys():
                    p = centroids[cf]['points']

                    p.append(Point(xc, yc, percentage, int(cf)))
                else:
                    centroids[cf] = {
                        'points': [Point(xc, yc, percentage, int(cf))]
                    }

        if centroids.__len__() > 3:
            rf = str(int(cf) - 3)
            centroids.pop(rf)

        cs = centroids[cf]['points']
        if centroids.__len__() > 2:
            cs_pre = centroids[str(int(cf) - 1)]['points']
            for p in cs_pre:
                counter = 1
                found = False
                parked = False
                moved = True
                for c in cs:
                    close = distance(p.x, p.y, c.x, c.y)
                    if close < 15:
                        found = True
                        if counter == 2:
                            print('Double')
                        else:
                            counter += 1
                        if int(cf) > p.here + 40:
                            parked = True

                            if not c.moved:
                                d = distance(p.startx, p.starty, c.startx, c.starty)
                                if d >= 100:
                                    moved = True
                                    c.moved = moved
                                    print('Car Moved')
                            #print('CAR PARKED')

                        centroids[cf]['points'].remove(c)
                        c.startx = p.startx
                        c.starty = p.starty
                        c.parked = parked
                        c.timer = 0
                        c.here = p.here
                        centroids[cf]['points'].append(c)

                    break
                if not found and p.parked and p.moved:
                    p.timer += 1
                    centroids[cf]['points'].append(p)
                    if p.timer > 40:
                        print('Parking space found')
                        centroids[cf]['points'].remove(p)

        # cs = centroids[cf]['points']
        # length = cs.__len__()
        # for i in range(length):
        #     # for j in range(i + 1, length):
        #     #     a1 = cs[i].x
        #     #     b1 = cs[i].y
        #     #     a2 = cs[j].x
        #     #     b2 = cs[j].y
        #     #     dist = distance(a1, b1, a2, b2)
        #     #     if dist < 155:
        #     #         if not cs[i].nextTo.__contains__(dist):
        #     #             cs[i].nextTo.append(dist)
        #     #         if not cs[j].nextTo.__contains__(dist):
        #     #             cs[j].nextTo.append(dist)
        #     found = False
        #     if centroids.__len__() > 2:
        #         cs_pre = centroids[str(int(cf) - 1)]['points']
        #         for csp in cs_pre:
        #             close = distance(cs[i].x, cs[i].y, csp.x, csp.y)
        #             if close < 15:
        #                 found = True
        #         if not found:
        #             if cs[i].timer > 20:
        #                 print('Car moved')
        #             else:
        #                 cs[i].timer = cs_pre[i]

        # print(str(cf) + ",", *centroids[str(cf)]['points'])
        print("frame " + cf)
        for d in cs:
            print(d)

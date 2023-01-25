import time

import cv2
from persondetection import DetectorAPI

video = cv2.VideoCapture(0)
odapi = DetectorAPI()
threshold = 0.7
max_acc3 = 0
x3 = 0
max_count3 = 0
while True:
    check, frame = video.read()
    img = cv2.resize(frame, (800, 600))
    boxes = odapi.processFrame(img)
    person = 0
    acc = 0
    for i in range(len(boxes)):

            box = boxes[i]
            person += 1
            cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED


    if (person > max_count3):
        max_count3 = person


    cv2.imshow("Human Detection from Camera", img)
    key = cv2.waitKey(1)
    time.sleep(2)
    if key & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows()





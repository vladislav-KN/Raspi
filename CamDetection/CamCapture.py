import time

from PIL import ImageTk, Image
import cv2
import argparse
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
    boxes, scores, classes, num = odapi.processFrame(img)
    person = 0
    acc = 0
    for i in range(len(boxes)):
        if classes[i] == 1 and scores[i] > threshold:
            box = boxes[i]
            person += 1
            cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)  # cv2.FILLED
            cv2.putText(img, f'P{person, round(scores[i], 2)}', (box[1] - 30, box[0] - 8),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)  # (75,0,130),
            acc += scores[i]
            if (scores[i] > max_acc3):
                max_acc3 = scores[i]

    if (person > max_count3):
        max_count3 = person


    cv2.imshow("Human Detection from Camera", img)
    key = cv2.waitKey(1)
    time.sleep(2)
    if key & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows()





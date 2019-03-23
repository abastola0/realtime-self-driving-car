
# import the necessary packages
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture('http://192.168.43.1:8080/video')
#loop over the image frames
while True:
        # load the frame and resize it to (1) reduce detection time
        # and (2) improve detection accuracy
        _,image = cap.read()
        image = imutils.resize(image, width=min(400, image.shape[1]))
 
        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                padding=(8, 8), scale=1.05)
 
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
 
        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
                cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        if len(pick):
                print('no of pedestrians detected:{}'.format(len(pick)))
 
        # show some information on the number of bounding boxes
        ##      filename = imagePath[imagePath.rfind("/") + 1:]
        ##      print("[INFO] {}: {} original boxes, {} after suppression".format(
        ##              filename, len(rects), len(pick)))
        
        # show the output images
        ##      cv2.imshow("Before NMS", orig)
        cv2.imshow("After NMS", image)
        if cv2.waitKey(1) & 0XFF == ord('g'):
                break

cv2.destroyAllWindows()
cap.release()

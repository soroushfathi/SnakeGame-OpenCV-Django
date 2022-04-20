import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 620)
handdetector = HandDetector(detectionCon=0.8, maxHands=2)
facedetector = FaceDetector(minDetectionCon=0.5)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hand, img = handdetector.findHands(img)
    img, bboxs = facedetector.findFaces(img)
    cv2.imshow('Game', img)
    cv2.waitKey(1)


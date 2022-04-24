import math
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 620)
handdet = HandDetector(detectionCon=0.8, maxHands=2)
facedet = FaceDetector(minDetectionCon=0.5)
facemeshdet = FaceMeshDetector(minDetectionCon=0.6)
posedet = PoseDetector(detectionCon=0.5)


class SnakeGame:
    def __init__(self):
        self.points = []
        self.distances = []  # distance between each point
        self.currlenght = 0  # total lenght of snake
        self.minlenght = 100
        self.prepoint = 0, 0  # previous point

    def update(self, img, newpoint):
        px, py = self.prepoint
        nx, ny = newpoint
        self.points.append([nx, ny])
        distance = math.hypot(nx - px, ny - py)
        self.distances.append(distance)
        self.currlenght += distance
        self.prepoint = nx, ny

        # draw snake
        for i, point in enumerate(self.points):
            if i != 0:
                cv2.line(img, self.points[i-1], self.points[i], (0, 0, 255), 7)
        cv2.circle(img, pointIndex, 8, (200, 0, 200), cv2.FILLED)
        return img


game = SnakeGame()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = handdet.findHands(img)
    # img, bboxs = facedetector.findFaces(img)
    # img, bboxs = facemeshdet.findFaceMesh(img)
    img = posedet.findPose(img, draw=True)
    if hands:
        lmlist = hands[0]['lmList']
        # print(lmlist)
        pointIndex = lmlist[8][:2]  # get (x, y) of pointer finger
        img = game.update(img, pointIndex)
    cv2.imshow('Game', img)
    cv2.waitKey(1)

import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1500)
cap.set(4, 800)
handdet = HandDetector(detectionCon=0.8, maxHands=2)
facedet = FaceDetector(minDetectionCon=0.5)
facemeshdet = FaceMeshDetector(minDetectionCon=0.6)
posedet = PoseDetector(detectionCon=0.5)


class SnakeGame:
    def __init__(self, foodpath):
        self.points = []
        self.distances = []  # distance between each point
        self.currlength = 0  # total lenght of snake
        self.allowedlength = 150
        self.prepoint = 0, 0  # previous point
        self.score = 0
        self.foodimg = cv2.imread(foodpath, cv2.IMREAD_UNCHANGED)
        self.hfood, self.wfood, _ = self.foodimg.shape
        self.foodpoint = 0, 0
        self.randomFoodLocation()

    def randomFoodLocation(self):
        self.foodpoint = random.randint(100, 1400), random.randint(100, 700)

    def update(self, img, newpoint):
        px, py = self.prepoint
        nx, ny = newpoint
        self.points.append([nx, ny])
        distance = math.hypot(nx - px, ny - py)
        self.distances.append(distance)
        self.currlength += distance
        self.prepoint = nx, ny

        # length reduction
        if self.currlength > self.allowedlength:
            for i, dis in enumerate(self.distances):
                self.currlength -= self.distances[i]
                self.distances.pop(i)
                self.points.pop(i)
                if self.currlength <= self.allowedlength:
                    break

        # Check the Snake ate the Food
        rx, ry = self.foodpoint
        if rx - self.wfood//2 < nx < rx + self.wfood//2 and ry - self.hfood//2 < ny < ry + self.hfood//2:
            self.randomFoodLocation()
            self.allowedlength += 50
            self.score += 1

        # Check for conclution
        # todo

        # Draw Snake
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:
                    cv2.line(img, self.points[i-1], self.points[i], (0, 100, 0), 22)
            cv2.circle(img, pointIndex, 8, (200, 0, 200), cv2.FILLED)

        # Draw Food
        rx, ry = self.foodpoint
        img = cvzone.overlayPNG(img, self.foodimg, (rx - self.wfood//2, ry - self.hfood//2))
        cv2.rectangle(img, (rx - self.wfood // 2, ry - self.hfood // 2), (rx + self.wfood // 2, ry + self.hfood // 2), (0, 100, 50), 2)

        return img


game = SnakeGame("statics/star.png")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = handdet.findHands(img)
    # img, bboxs = facedetector.findFaces(img)
    # img, bboxs = facemeshdet.findFaceMesh(img)
    # img = posedet.findPose(img, draw=True)
    if hands:
        lmlist = hands[0]['lmList']
        # print(lmlist)
        pointIndex = lmlist[8][:2]  # get (x, y) of pointer finger
        img = game.update(img, pointIndex)
    cv2.imshow('Game', img)
    cv2.waitKey(1)

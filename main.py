import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PoseModule import PoseDetector
from PIL import Image, ImageFont, ImageDraw
import arabic_reshaper
from bidi.algorithm import get_display

cap = cv2.VideoCapture(0)
cap.set(3, 1500)
cap.set(4, 800)
handdet = HandDetector(detectionCon=0.8, maxHands=1)
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

        self.font = ImageFont.truetype('statics/Vazirmatn-Black.ttf', 40, encoding='unic')
        self.snakeimg = cv2.imread("statics/snake.png", cv2.IMREAD_UNCHANGED)
        self.hsnake, self.wsnake, _ = self.snakeimg.shape
        self.gameoverimg = cv2.imread("statics/gameover.png", cv2.IMREAD_UNCHANGED)
        self.hgameoverimg, self.wgameoverimg, _ = self.gameoverimg.shape
        self.gameoverimg2 = cv2.imread("statics/gameover2.png", cv2.IMREAD_UNCHANGED)
        self.hgameoverimg2, self.wgameoverimg2, _ = self.gameoverimg2.shape
        self.foodimg = cv2.imread(foodpath, cv2.IMREAD_UNCHANGED)
        self.hfood, self.wfood, _ = self.foodimg.shape
        self.foodpoint = 0, 0
        self.randomFoodLocation()
        self.gameover = False
        self.outofrange = False

    def randomFoodLocation(self):
        self.foodpoint = random.randint(100, 800), random.randint(100, 700)

    def update(self, img, newpoint):
        if self.outofrange and self.gameover:
            img = cvzone.overlayPNG(img, self.gameoverimg2, [100, 100])
            cvzone.putTextRect(img, f"Your Score: {self.score}", [480, 700], scale=2, thickness=2, offset=7)
        elif self.gameover:
            img = cvzone.overlayPNG(img, self.gameoverimg, [100, 100])
            cvzone.putTextRect(img, f"Your Score: {self.score}", [480, 700], scale=2, thickness=2, offset=7)
        else:
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

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(img, self.points[i-1], self.points[i], (0, 100, 0), 22)
                cv2.circle(img, pointIndex, 8, (200, 0, 200), cv2.FILLED)
            try:
                img = cvzone.overlayPNG(img, self.snakeimg, (nx - self.hsnake//2, ny - self.wsnake//2))
            except ValueError:
                self.gameover = True
                self.outofrange = True
                self.points = []
                self.distances = []  # distance between each point
                self.currlength = 0  # total lenght of snake
                self.allowedlength = 150
                self.prepoint = 0, 0  # previous point

            # Draw Food
            rx, ry = self.foodpoint
            img = cvzone.overlayPNG(img, self.foodimg, (rx - self.wfood//2, ry - self.hfood//2))
            # cv2.rectangle(img, (rx - self.wfood // 2, ry - self.hfood // 2), (rx + self.wfood // 2, ry + self.hfood // 2), (0, 100, 50), 2)

            # Check for conclution
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            # TODO line type
            cv2.polylines(img, [pts], False, (0, 200, 0), 4)
            mindis = cv2.pointPolygonTest(pts, (nx, ny), True)
            if -1.001 <= mindis <= 1.001:
                self.gameover = True
                self.points = []
                self.distances = []  # distance between each point
                self.currlength = 0  # total lenght of snake
                self.allowedlength = 150
                self.prepoint = 0, 0  # previous point

            cvzone.putTextRect(img, f"Score: {self.score}", [50, 80], scale=2, thickness=3, offset=10)

        return img


game = SnakeGame("statics/apple.png")

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
    else:
        pass
        # draw = ImageDraw.Draw(img)
        # text = "برای ادامه بازی دستت رو داخل صفحه قرار بده"
        # reshaped_text = arabic_reshaper.reshape(text)  # correct its shape
        # bidi_text = get_display(reshaped_text)  # correct its direction
        # draw.text((450, 700), bidi_text, (255, 2, 2), font=font)
    cv2.imshow('Game', img)
    key = cv2.waitKey(1)
    if key == ord('r') or key == ord('R'):
        game.gameover = False
        game.outofrange = False
        game.score = 0

from django.shortcuts import render
import math
import random
import cvzone
import cv2
import numpy as np
from screeninfo import get_monitors
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PoseModule import PoseDetector
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from PIL import Image, ImageFont, ImageDraw
from .models import record


class SnakeGame:
    def __init__(self, foodpath):
        self.points = []
        self.distances = []  # distance between each point
        self.currlength = 0  # total lenght of snake
        self.allowedlength = 150
        self.prepoint = 0, 0  # previous point
        self.score = 0
        self.maxscore = 0

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
        self.foodpoint = random.randint(200, 1000), random.randint(200, 600)

    def update(self, img, newpoint):
        if self.outofrange and self.gameover:
            img = cvzone.overlayPNG(img, self.gameoverimg2, [0, 0])
            cvzone.putTextRect(img, f"Your Score: {self.score}, max score: {self.maxscore}", [400, 700], scale=2,
                               thickness=2, offset=7)
        elif self.gameover:
            img = cvzone.overlayPNG(img, self.gameoverimg, [0, 0])
            cvzone.putTextRect(img, f"Your Score: {self.score}, max score: {self.maxscore}", [400, 700], scale=2,
                               thickness=2, offset=7)
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
            if rx - self.wfood // 2 < nx < rx + self.wfood // 2 and ry - self.hfood // 2 < ny < ry + self.hfood // 2:
                self.randomFoodLocation()
                self.allowedlength += 50
                self.score += 1

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(img, self.points[i - 1], self.points[i], (0, 100, 0), 22)
                cv2.circle(img, newpoint, 8, (200, 0, 200), cv2.FILLED)
            try:
                img = cvzone.overlayPNG(img, self.snakeimg, (nx - self.hsnake // 2, ny - self.wsnake // 2))
            except ValueError:
                self.outofrange = True
                self.gameover = True
                self.points = []
                self.distances = []  # distance between each point
                self.currlength = 0  # total lenght of snake
                self.allowedlength = 150
                self.prepoint = 0, 0  # previous point
                if self.score > self.maxscore:
                    self.maxscore = self.score

            # Draw Food
            rx, ry = self.foodpoint
            img = cvzone.overlayPNG(img, self.foodimg, (rx - self.wfood // 2, ry - self.hfood // 2))

            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            # TODO line type
            cv2.polylines(img, [pts], False, (0, 200, 0), 5)
            mindis = cv2.pointPolygonTest(pts, (nx, ny), True)
            if -1.01 <= mindis <= 1.01:
                self.gameover = True
                self.points = []
                self.distances = []  # distance between each point
                self.currlength = 0  # total lenght of snake
                self.allowedlength = 150
                self.prepoint = 0, 0  # previous point
                if self.score > self.maxscore:
                    self.maxscore = self.score

            cvzone.putTextRect(img, f"Score: {self.score}", [50, 80], scale=2, thickness=3, offset=10)

        return img


def gen(request, cap, game, handdet):
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = handdet.findHands(img)

        fingers = [True]
        if hands:
            lmlist = hands[0]['lmList']
            hand = hands[0]
            fingers = handdet.fingersUp(hand)

            pointIndex = lmlist[8][:2]  # get (x, y) of pointer finger
            img = game.update(img, pointIndex)
        key = cv2.waitKey(1)
        if key == ord('r') or key == ord('R') or not all(fingers):
            new_record = record(user=request.user, record=game.score)
            new_record.save()
            game.gameover = False
            game.outofrange = False
            game.score = 0
        _, jpeg = cv2.imencode('.jpg', img)
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n'


@gzip.gzip_page
def play(request):
    game = SnakeGame("statics/apple.png")
    try:
        cap = cv2.VideoCapture(0)
        screen = get_monitors().pop()
        cap.set(3, screen.width)
        cap.set(4, screen.height)
        handdet = HandDetector(detectionCon=0.8, maxHands=1)
        # facedet = FaceDetector(minDetectionCon=0.5)
        # facemeshdet = FaceMeshDetector(minDetectionCon=0.6)
        # posedet = PoseDetector(detectionCon=0.5)
        return StreamingHttpResponse(gen(cap, game, handdet), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        return StreamingHttpResponse(gen(request, cap, game, handdet), content_type="multipart/x-mixed-replace;boundary=frame")


def game_page(request):
    return render(request, 'game/game_page.html', context={})


def game_event(request):
    return render(request, 'game/game.html', context={})

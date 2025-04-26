import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import pygame

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

# Initialize sounds
pygame.mixer.init()
EAT_SOUND = pygame.mixer.Sound("eat.wav")
GAME_OVER_SOUND = pygame.mixer.Sound("game_over.wav")

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGameClass:
    def __init__(self, pathfood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point

        self.imgFood = cv2.imread(pathfood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.score = 0
        self.gameOver = False
        self.hand_moving = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 400), random.randint(100, 400)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 300], scale=2, thickness=3, offset=10)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 400], scale=2, thickness=3, offset=10)
            cvzone.putTextRect(imgMain, "Raise Pointer to Play Again", [300, 500], scale=2, thickness=2, offset=10)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            # Detect if hand is moving
            if math.hypot(cx - px, cy - py) > 5:  # Threshold for hand movement
                self.hand_moving = True
            else:
                self.hand_moving = False

            if self.hand_moving:
                self.points.append([cx, cy])
                distance = math.hypot(cx - px, cy - py)
                self.lengths.append(distance)
                self.currentLength += distance
                self.previousHead = cx, cy

                # Length Reduction
                if self.currentLength > self.allowedLength:
                    for i, length in enumerate(self.lengths):
                        self.currentLength -= length
                        self.lengths.pop(i)
                        self.points.pop(i)
                        if self.currentLength < self.allowedLength:
                            break

            # Check if snake ate the food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 20
                self.score += 1
                EAT_SOUND.play()

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)

            # Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.wFood // 2, ry - self.hFood // 2))

            cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
                               scale=3, thickness=3, offset=10)

            # Check for Collision
            if len(self.points) > 10:  # Start checking collision after a minimum length
                pts = np.array(self.points[:-2], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
                minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

                if -1 <= minDist <= 1:
                    self.gameOver = True
                    self.points = []  # reset snake
                    self.lengths = []  # reset lengths
                    self.currentLength = 0  # reset length
                    self.allowedLength = 150  # reset allowed length
                    self.previousHead = 0, 0  # reset head
                    GAME_OVER_SOUND.play()
                    self.randomFoodLocation()

        return imgMain

# Initialize the game
game = SnakeGameClass("linkedin.png")

while True:
    try:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False, draw=False)  # Disabled hand drawing

        if hands:
            lmList = hands[0]['lmList']
            pointIndex = lmList[8][0:2]
            img = game.update(img, pointIndex)

            # Restart the game if pointer finger is raised
            fingers = detector.fingersUp(hands[0])
            if fingers == [0, 1, 0, 0, 0] and game.gameOver:  # Pointer finger raised
                game.gameOver = False
                game.score = 0

        cv2.imshow("Snake Game", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    except Exception as e:
        print("An error occurred:", str(e))
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

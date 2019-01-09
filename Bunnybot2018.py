import libjevois as jevois
import cv2
import numpy as np
import pickle
from enum import Enum


class BallColor(Enum):
    NONE = 0
    RED = 1
    BLUE = 2


class Bunnybot2018:
    def __init__(self):
        self.min_blue_threshold = np.array([90, 0, 0], dtype=np.uint8)
        self.max_blue_threshold = np.array([115, 240, 240], dtype=np.uint8)
        self.min_red_threshold = np.array([5, 240, 240], dtype=np.uint8)
        self.max_red_threshold = np.array([165, 40, 40], dtype=np.uint8)
        self.red_0_threshold = np.array([0, 20, 20], dtype=np.uint8)
        self.red_360_threshold = np.array([180, 240, 240], dtype=np.uint8)
        self.mask_only = False

        self.radius_filter = 25

        self.width = 320
        self.height = 240

    def detect(self, img_hsv):
        red_mask, blue_mask = self.create_masks(img_hsv)
        red_contours, blue_contours = self.find_contours(red_mask, blue_mask)

        red_radius = 0.0
        blue_radius = 0.0

        if len(blue_contours) > 0:
            _, radius = cv2.minEnclosingCircle(blue_contours[0])
            if radius > self.radius_filter:
                blue_radius = radius
        if len(red_contours) > 0:
            _, radius = cv2.minEnclosingCircle(red_contours[0])
            if radius > self.radius_filter:
                red_radius = radius

        if red_radius > blue_radius:
            return BallColor.RED
        elif blue_radius > red_radius:
            return BallColor.BLUE
        return BallColor.NONE

    def create_masks(self, img_hsv):
        # Create mask
        blue_mask = cv2.inRange(
            img_hsv, self.min_blue_threshold, self.max_blue_threshold
        )

        redlow_mask = cv2.inRange(img_hsv, self.red_0_threshold, self.min_red_threshold)
        redhigh_mask = cv2.inRange(
            img_hsv, self.max_red_threshold, self.red_360_threshold
        )
        red_mask = cv2.bitwise_or(redlow_mask, redhigh_mask)

        return red_mask, blue_mask

    def find_contours(self, red_mask, blue_mask):
        _, blue_contours, _ = cv2.findContours(
            blue_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        _, red_contours, _ = cv2.findContours(
            red_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        blue_contours = sorted(blue_contours, key=cv2.contourArea, reverse=True)
        red_contours = sorted(red_contours, key=cv2.contourArea, reverse=True)

        return red_contours, blue_contours

    def process(self, inframe, outframe):
        in_bgr = inframe.getCvBGR()

        # Convert input image to HSV for output:
        img_hsv = cv2.cvtColor(in_bgr, cv2.COLOR_BGR2HSV)

        red_mask, blue_mask = self.create_masks(img_hsv)
        red_contours, blue_contours = self.find_contours(red_mask, blue_mask)

        if not self.mask_only:
            if len(blue_contours) > 0:
                (x, y), radius = cv2.minEnclosingCircle(blue_contours[0])
                if radius >= self.radius_filter:
                    cv2.circle(img_hsv, (int(x), int(y)), int(radius), (0, 0, 255))

            if len(red_contours) > 0:
                (x, y), radius = cv2.minEnclosingCircle(red_contours[0])
                if radius >= self.radius_filter:
                    cv2.circle(img_hsv, (int(x), int(y)), int(radius), (255, 0, 0))
            bgr_img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        else:
            mask = cv2.bitwise_or(red_mask, blue_mask)
            masked_img = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)
            bgr_img = cv2.cvtColor(masked_img, cv2.COLOR_HSV2BGR)

        outframe.sendCvBGR(bgr_img)

    def processNoUSB(self, inframe):
        in_bgr = inframe.getCvBGR()

        # Convert input image to HSV for output:
        img_hsv = cv2.cvtColor(in_bgr, cv2.COLOR_BGR2HSV)

        ball_color = self.detect(img_hsv)
        self.send_serial(ball_color)

    def send_serial(self, color):
        if color == BallColor.RED:
            jevois.sendSerial("RED")
        elif color == BallColor.BLUE:
            jevois.sendSerial("BLUE")
        else:
            jevois.sendSerial("NONE")

    def parseSerial(self, msg: str):
        if msg.startswith("set-mask"):
            self.set_mask_only(msg[9:])
            return ""
        else:
            return "ERR: Unsupported command"

    def set_mask_only(self, val: str) -> str:
        if val == "on":
            self.mask_only = True
        elif val == "off":
            self.mask_only = False
        else:
            return "Unrecognized option for 'set-mask': %s" % val

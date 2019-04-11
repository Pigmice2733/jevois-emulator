"""
Mock libjevois library
"""
from typing import Callable
import cv2
import numpy as np

kill = lambda _: ()

V4L2_PIX_FMT_YUYV = 0
V4L2_PIX_FMT_RGB = 1


def _initialize_module(kill_handle: Callable[[], None]):
    global kill
    kill = kill_handle


def sendSerial(msg: str):
    print(msg)


def LINFO(msg: str):
    print(msg)


def LFATAL(msg: str):
    print(msg)
    kill()


def convertToCvGray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def convertToCvBGR(img):
    return img


def paste(orig, dest, x, y):
    dest[y : y + orig.shape[0], x : x + orig.shape[1]] = orig


class Inframe:
    def __init__(self, image):
        self.image = image

    def getCvBGR(self):
        return self.image

    def get(self):
        return self.image

    def done(self):
        pass


class YUYV:
    Black = np.uint8(0x8000)
    DarkGrey = np.uint8(0x8050)
    MedGrey = np.uint8(0x8080)
    LightGrey = np.uint8(0x80A0)
    White = np.uint8(0x80FF)
    DarkGreen = np.uint8(0x0000)
    MedGreen = np.uint8(0x0040)
    LightGreen = np.uint8(0x00FF)
    DarkTeal = np.uint8(0x7070)
    MedTeal = np.uint8(0x7090)
    LightTeal = np.uint8(0x70B0)
    DarkPurple = np.uint8(0xA030)
    MedPurple = np.uint8(0xA050)
    LightPurple = np.uint8(0xA080)
    DarkPink = np.uint8(0xFF00)
    MedPink = np.uint8(0xFF80)
    LightPink = np.uint8(0xFFFF)


class RawImage:
    def __init__(self):
        self.image = np.zeros((100, 100, 3), np.uint8)
        self._width = 100
        self._height = 100
        self._format = V4L2_PIX_FMT_RGB
        self._valid = True

    def require(self, w, h, f):
        self._width = w
        self._height = h
        self._format = f

        if f == V4L2_PIX_FMT_YUYV:
            self.image = np.zeros((h, w, 4), np.uint8)
            self._valid = True
        elif f == V4L2_PIX_FMT_RGB:
            self.image = np.zeros((h, w, 3), np.uint8)
            self._valid = True
        else:
            self._valid = False
            raise ValueError("Format {} is not supported".format(f))

    def width(self):
        return self._width

    def height(self):
        return self._height

    def fps(self):
        raise NotImplementedError()

    def fmt(self):
        return self._format

    def valid(self):
        return self._valid


class Outframe:
    def __init__(self):
        self.image = None

    def sendCvBGR(self, image):
        self.image = image

    def get(self):
        self.image = RawImage()
        return self.image

    def _retrieve(self):
        if isinstance(self.image, RawImage):
            return self.image.image
        return self.image

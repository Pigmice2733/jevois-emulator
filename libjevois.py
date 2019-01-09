"""
Mock libjevois library
"""


def sendSerial(output: str):
    print(output)


class Inframe:
    def __init__(self, image):
        self.image = image

    def getCvBGR(self):
        return self.image


class Outframe:
    def __init__(self):
        self.image = None

    def sendCvBGR(self, image):
        self.image = image

import cv2
import libjevois
import argparse
import importlib

def parse_args():
    parser = argparse.ArgumentParser(description="Emulator for JeVois camera")
    parser.add_argument("--module", help="Name of vision module", default="Vision")
    args = parser.parse_args()
    return args

def load_vision_module(args):
    module = importlib.import_module(args.module + "." + args.module)
    vision_class = getattr(module, args.module)
    return vision_class()

class Main:
    display_output = True
    video_capture = None
    retval = None

    def __init__(self, window_title, vision_module):
        cv2.namedWindow(window_title)
        cv2.createTrackbar("Output", window_title, 0, 1, self.handle_output_toggle)

        self.vision_module = vision_module
        self.window_title = window_title

        self.init_video()

    def handle_output_toggle(self, val):
        self.display_output = val == 0

    def init_video(self):
        self.video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if self.video_capture.isOpened():
            self.retval, _ = self.video_capture.read()
        else:
            print("Couldn't read frame from camera.")
            self.retval = False

    def release(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

    def kill(self):
        self.retval = False

    def start(self):
        try:
            while self.retval:
                self.retval, frame = self.video_capture.read()
                inframe = libjevois.Inframe(frame)
                outframe = libjevois.Outframe()

                if self.display_output:
                    self.vision_module.process(inframe, outframe)
                    cv2.imshow(self.window_title, outframe._retrieve())
                else:
                    self.vision_module.processNoUSB(inframe)
                    cv2.imshow(self.window_title, frame)

                key = cv2.waitKey(20)
                if key == 27:
                    break

        except KeyboardInterrupt:
            pass

args = parse_args()
vision_module = load_vision_module(args)

emulator = Main("JeVois Emulator", vision_module)
libjevois._initialize_module(emulator.kill)

emulator.start()
emulator.release()

import cv2
import libjevois
import Bunnybot2018
import argparse
import importlib

display_output = True
video_capture = None
retval = None


def parse_args():
    parser = argparse.ArgumentParser(description="Emulator for JeVois camera")
    parser.add_argument("--module", help="Name of vision module", default="Vision")
    args = parser.parse_args()
    return args


def load_vision_module(args):
    module = importlib.import_module(args.module)
    vision_class = getattr(module, args.module)
    return vision_class()


def handle_output_toggle(val):
    global display_output
    display_output = val == 0


def create_window(window_title: str):
    cv2.namedWindow(window_title)
    cv2.createTrackbar("Output", window_title, 0, 1, handle_output_toggle)


def init_video():
    global video_capture
    global retval
    video_capture = cv2.VideoCapture(0)
    if video_capture.isOpened():
        retval, _ = video_capture.read()
    else:
        print("Couldn't read frame from camera.")
        retval = False


def release():
    global video_capture
    video_capture.release()
    cv2.destroyAllWindows()


window_title = "JeVois Emulator"

args = parse_args()
vision = load_vision_module(args)
create_window(window_title)
init_video()

try:
    while retval:
        retval, frame = video_capture.read()
        inframe = libjevois.Inframe(frame)
        outframe = libjevois.Outframe()

        if display_output:
            vision.process(inframe, outframe)
            cv2.imshow(window_title, outframe.image)
        else:
            vision.processNoUSB(inframe)
            cv2.imshow(window_title, frame)

        key = cv2.waitKey(20)
        if key == 27:
            break

except KeyboardInterrupt:
    pass

release()

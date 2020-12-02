import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCREEN = "main_screen"
MAIN_SCREEN_PATH = os.path.join(CUR_DIR, "gui", 'kiv', "main_screen.kv")
BAD_FRAME_PATH = os.path.join(CUR_DIR, 'utils', 'img', 'bad_camera.png')
VIDEO_PATH = ""

BLUR_THRESH = 150
GOOD_MATCH_NUMBER = 5
MAX_SIZE = 10
DIRECTION_THRESH = 5
BAUD_RATE = 115200

ARDUINO_PORT = "COM11"

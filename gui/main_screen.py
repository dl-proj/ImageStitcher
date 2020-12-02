import queue
import threading
# import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from src.edge.stitcher import EdgeTracker
# from src.motor.serial_com import ArduinoCom
from src.motor.director import get_motor_direction_frame
from settings import MAIN_SCREEN_PATH, MAX_SIZE


Builder.load_file(MAIN_SCREEN_PATH)


class MainScreen(Screen):
    capture = None
    event_take_video = None
    texture = None

    def __init__(self, **kwargs):

        super(MainScreen, self).__init__(**kwargs)
        self.frame_queue = queue.Queue(MAX_SIZE)
        self.pre_direction = ""
        self.motor_thread_stop = False
        self.stop_ret = False

        # self.motor_controller = ArduinoCom()
        self.stitch_thread = None
        self.edge_stitch = EdgeTracker(queue_=self.frame_queue)
        self.edge_stitch.start()

    def on_enter(self, *args):
        self.ids.video.start()
        self.edge_stitch.resume()

    def on_leave(self, *args):
        self.ids.video.stop()
        self.edge_stitch.pause()
        super(MainScreen, self).on_leave(*args)

    def stitch_image_motor_control(self):
        self.stitch_thread = threading.Thread(target=self._start_motor_control)
        self.stitch_thread.start()

    def _start_motor_control(self):

        self.ids.video.reset_overlay()
        self.edge_stitch.stitched_frame = None
        self.stop_ret = False

        while not self.stop_ret:
            if self.motor_thread_stop:
                break
            frame = self.ids.video.get_frame()
            motor_direction, self.pre_direction, _ = \
                get_motor_direction_frame(frame=frame, thresh_value=int(self.ids.label2.text),
                                          prev_direction=self.pre_direction)
            print(motor_direction)
            motor_res = self.motor_controller.communicate_arduino(direction=motor_direction)
            print(motor_res)
            # time.sleep(5)
            if motor_res != "":
                self.frame_queue.put(frame)

    def _stop_motor_control(self):
        self.stop_ret = True
        self.stitch_thread.join()

    def show_stitched_result(self):
        stitched_frame = self.edge_stitch.extract_result(thresh_value=int(self.ids.label2.text))
        self.ids.video.set_overlay(frame=stitched_frame)

        return

    def close_window(self):
        self.motor_controller.close_port()
        self.motor_thread_stop = True
        App.get_running_app().stop()

    def on_close(self):
        pass

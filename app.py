from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from gui.main_screen import MainScreen
from settings import MAIN_SCREEN


class EdgeTrackingTool(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_screen = MainScreen(name=MAIN_SCREEN)

        screens = [
            self.main_screen
        ]

        self.sm = ScreenManager()
        for screen in screens:
            self.sm.add_widget(screen)

    def build(self):
        self.sm.current = MAIN_SCREEN

        return self.sm

    def on_stop(self):
        self.main_screen.edge_stitch.stop()
        self.main_screen.edge_stitch.join()
        self.main_screen.stop_ret = True
        self.main_screen.stitch_thread.join()
        Window.close()


if __name__ == '__main__':

    EdgeTrackingTool().run()

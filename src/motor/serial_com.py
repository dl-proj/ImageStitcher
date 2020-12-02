import serial
import time

from settings import ARDUINO_PORT, BAUD_RATE


class ArduinoCom:

    def __init__(self):

        self.ard = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=5)
        time.sleep(2)

    def communicate_arduino(self, direction):

        direction += "\n"
        self.ard.write(direction.encode("utf-8"))
        while True:
            response = self.ard.read(self.ard.inWaiting())
            if response:
                break
        response = response.decode().replace("\r\n", "")

        return response

    def close_port(self):

        if self.ard.isOpen():
            self.ard.close()


if __name__ == '__main__':

    for i in range(3):
        res = ArduinoCom().communicate_arduino(direction="x1y2")
        print(res)

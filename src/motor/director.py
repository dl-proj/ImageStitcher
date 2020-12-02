import cv2
import numpy as np

from settings import DIRECTION_THRESH

kernel = np.ones((10, 10), np.uint8)


def get_motor_direction_frame(frame, thresh_value, prev_direction):

    stop_ret = False

    height, width = frame.shape[:2]
    window_scale = width / height
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, frame_thresh = cv2.threshold(frame_gray, thresh_value, 255, cv2.THRESH_BINARY)
    frame_erode = cv2.erode(frame_thresh, kernel, iterations=1)
    frame_dilate = cv2.dilate(frame_erode, kernel, iterations=3)
    # cv2.imshow("frame dilate", frame_dilate)
    # cv2.waitKey()
    edges = cv2.Canny(frame_dilate, 100, 200)
    edge_dilate = cv2.dilate(edges, kernel, iterations=2)
    # cv2.imshow("thresh frame", edge_dilate)
    # cv2.waitKey()
    min_line_length = height * 0.2
    max_line_gap = 100
    lines = cv2.HoughLinesP(edge_dilate, 1, np.pi / 180, 100, min_line_length, max_line_gap)
    if lines is not None:
        lines_length = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            line_length = abs(x2 - x1) ^ 2 + abs(y2 - y1) ^ 2
            lines_length.append(line_length)
        max_idx = lines_length.index(max(lines_length))
        max_x1, max_y1, max_x2, max_y2 = lines[max_idx][0]
        # cv2.line(frame, (max_x1, max_y1), (max_x2, max_y2), (0, 0, 255), 2)
        center_point = [int(0.5 * (max_x1 + max_x2)), int(0.5 * (max_y1 + max_y2))]
        left_point = frame_dilate[center_point[1], max(center_point[0] - int(width / 4), 1)]
        right_point = frame_dilate[center_point[1], min(center_point[0] + int(width / 4), width - 1)]
        top_point = frame_dilate[max(center_point[1] - int(height / 4), 1), center_point[0]]
        bottom_point = frame_dilate[min(center_point[1] + int(height / 4), height - 1), center_point[0]]
        grad = abs(max_x2 - max_x1) / (abs(max_y2 - max_y1) * window_scale)
        if grad > DIRECTION_THRESH:
            if top_point == 0 and bottom_point == 255:
                direction = "x1"
                if center_point[1] > height / 2:
                    direction += "y1"
                else:
                    direction += "y2"
            else:
                direction = "x2"
                if center_point[1] > height / 2:
                    direction += "y1"
                else:
                    direction += "y2"
        elif grad < 1 / DIRECTION_THRESH:
            if left_point == 0 and right_point == 255:
                direction = "y2"
                if center_point[0] > width / 2:
                    direction = "x1" + direction
                else:
                    direction = "x2" + direction
            else:
                direction = "y1"
                if center_point[0] > width / 2:
                    direction = "x1" + direction
                else:
                    direction = "x2" + direction
        else:
            if top_point == 0 and bottom_point == 255:
                direction = "x1"
            else:
                direction = "x2"
            if left_point == 0 and right_point == 255:
                direction += "y2"
            else:
                direction += "y1"
    else:
        direction = prev_direction

    if direction == "x1" and prev_direction == "y2":
        stop_ret = True
    prev_direction = direction
    # print(direction)
    # cv2.imshow("frame line", frame)
    # cv2.waitKey()

    return direction, prev_direction, stop_ret


if __name__ == '__main__':

    cap = cv2.VideoCapture("")
    while True:
        _, image = cap.read()
        get_motor_direction_frame(frame=image, thresh_value=80, prev_direction="")

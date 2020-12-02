import cv2

from utils.folder_file_manager import log_print


def detect_edge_frame(frame, thresh_value):

    try:

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, frame_thresh = cv2.threshold(frame_gray, thresh_value, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(frame_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contour = sorted(contours, key=cv2.contourArea, reverse=True)
        edge_frame = cv2.drawContours(frame, [sorted_contour[0]], 0, (0, 0, 255), 2)
        edge_only_frame = cv2.rectangle(edge_frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), 3)
        return edge_only_frame
    except Exception as e:
        log_print(info_str=e)


if __name__ == '__main__':

    detect_edge_frame(frame=cv2.imread(""), thresh_value=71)

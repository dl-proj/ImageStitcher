import cv2
import time
import numpy as np
import threading
import queue
# import os
# import ntpath

from src.edge.feature_key_point import KeyPointOffset
from utils.folder_file_manager import log_print
from settings import BLUR_THRESH


class EdgeTracker(threading.Thread):

    def __init__(self, queue_):

        super(EdgeTracker, self).__init__()

        self._stopped = threading.Event()
        self._stopped.clear()
        self._paused = threading.Event()
        self._paused.clear()
        self.feature_extractor = KeyPointOffset()
        self.prev_offset = np.zeros(2, dtype=np.int)
        self.stitched_frame = None
        self.first_frame = None
        self.second_frame = None
        self.frame_queue = queue_

    def pause(self):
        self._paused.set()

    def resume(self):
        self._paused.clear()

    def stop(self):
        self._stopped.set()

    def run(self, paths=None):

        if paths is None:
            while True:
                if self._stopped.isSet():
                    break

                try:
                    self.second_frame = self.frame_queue.get(timeout=0.1)
                    if self._stopped.isSet():
                        break
                except Exception as e:
                    log_print(e)
                    time.sleep(0.2)
                    continue

                frame_gray = cv2.cvtColor(self.second_frame, cv2.COLOR_BGR2GRAY)
                # cv2.imshow("frame", self.second_frame)
                blur_value = cv2.Laplacian(frame_gray, cv2.CV_64F).var()
                print(blur_value)
                if blur_value > BLUR_THRESH:
                    if self.first_frame is not None:
                        self.stitched_frame = self.stitch_two_frames(f_frame=self.first_frame,
                                                                     s_frame=self.second_frame)
                        # cv2.imshow("stitch frame", cv2.resize(self.stitched_frame, None, fx=0.2, fy=0.2))
                        # if cv2.waitKey(1) & 0xFF == ord('q'):
                        #     break
                    self.first_frame = self.second_frame
                # cv2.imshow("stitched frame", cv2.resize(self.stitched_frame, (800, 600)))

        else:
            pass

            # for i in range(len(paths) - 1):
            #     left_path = paths[i]
            #     right_path = paths[i + 1]
            #     img_left = cv2.imread(left_path)
            #     img_right = cv2.imread(right_path)
            #     stitched = self.stitch_two_frames(f_frame=img_left, s_frame=img_right)
            # cv2.imwrite("stitched_{}_{}.jpg".format(i, i + 1), stitched)
            # cv2.imshow("stitched frame", stitched)
            # cv2.waitKey()

    def extract_result(self, thresh_value):

        stitch_gray = cv2.cvtColor(self.stitched_frame, cv2.COLOR_BGR2GRAY)
        _, stitch_thresh = cv2.threshold(stitch_gray, thresh_value, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(stitch_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contour = sorted(contours, key=cv2.contourArea, reverse=True)
        result_frame = cv2.drawContours(self.stitched_frame, [sorted_contour[0]], 0, (0, 255, 0), 2)

        return result_frame

    def stitch_two_frames(self, f_frame, s_frame):

        ret, [offset, kps_pos1, _] = self.feature_extractor.calc_offset(l_img=f_frame, r_img=s_frame)

        if not ret:
            return self.stitched_frame

        else:
            # origin_offset = offset.copy()
            offset += self.prev_offset
            kps_pos1 += self.prev_offset

            if self.stitched_frame is None:
                self.stitched_frame = self.stitch(img_left=f_frame, img_right=s_frame, offset=offset, kps_pos=kps_pos1)
            else:
                self.stitched_frame = self.stitch(img_left=self.stitched_frame, img_right=s_frame, offset=offset,
                                                  kps_pos=kps_pos1)

            self.prev_offset = offset

            return self.stitched_frame

    @staticmethod
    def stitch(img_left, img_right, offset, kps_pos):

        img_left_h, img_left_w = img_left.shape[:2]
        img_right_h, img_right_w = img_right.shape[:2]
        # print(origin_offset)
        # print(offset)
        # print(kps_pos)

        dst_sz_w = max(offset[0] + img_right_w, img_left_w)
        dst_sz_h = max(offset[1] + img_right_h, img_left_h)

        dst_img = np.zeros((dst_sz_h, dst_sz_w, 3), dtype=np.uint8)

        trans_matrix = np.float32([
            [1, 0, offset[0]],
            [0, 1, offset[1]]
        ])
        trans_1 = dst_img.copy()
        trans_1[:img_left_h, :img_left_w] = img_left
        # trans_1[:img_left_h, dst_sz_w - img_left_w:] = img_left
        trans_2 = cv2.warpAffine(img_right, trans_matrix, (dst_sz_w, dst_sz_h))
        # cv2.imshow("tran1 image", trans_1)
        # cv2.imshow("warpin image", trans_2)
        # cv2.waitKey()
        # print(trans_1.shape[:2])

        # dst_img[:, :kps_pos[0]] = trans_1[:, :kps_pos[0]]
        # dst_img[:, kps_pos[0]:] = trans_2[:, kps_pos[0]:]

        # smoothing edge
        mask = np.zeros_like(dst_img, dtype=np.uint8)
        # y_blur_top = max(int(0.5 * (offset[1] - origin_offset[1] + offset[1] + img_right_h)), 0)
        y_blur_bottom = min(offset[1] + img_right_h, dst_sz_h)
        # x_blur_left = max(int(0.5 * (offset[0] - origin_offset[0] + offset[0] + img_right_w)), 0)
        x_blur_right = min(offset[0] + img_right_w, dst_sz_w)
        # print(x_blur_left, y_blur_top, x_blur_right, y_blur_bottom)
        # mask[:, :kps_pos[0]] = (255, 255, 255)
        mask[kps_pos[1]:y_blur_bottom, max(offset[0] + 10, 0):min(offset[0] + img_right_w, dst_sz_w)] = (255, 255, 255)
        mask[max(offset[1] + 10, 0):min(offset[1] + img_right_h, dst_sz_h), kps_pos[0]:x_blur_right] = (255, 255, 255)
        blur_mask = cv2.GaussianBlur(mask, (15, 15), 0)
        # print(blur_mask.shape[:2])
        # cv2.imshow("blur", blur_mask)
        # cv2.waitKey(0)

        blur_mask = blur_mask.astype(np.float)

        dst_img = trans_1 * (1 - blur_mask / 255.0) + trans_2 * (blur_mask / 255.0)
        dst_img = dst_img.astype(np.uint8)

        return dst_img


if __name__ == '__main__':

    cap = cv2.VideoCapture("")
    frame_queue = queue.Queue(10)
    edge_stitch = EdgeTracker(queue_=frame_queue)
    edge_stitch.start()
    while True:
        try:
            _, frame = cap.read()
            frame_queue.put(frame)
        except frame_queue.full():
            time.sleep(0.2)
    # folder = ""
    # img_paths = [os.path.join(folder, fn) for fn in os.listdir(folder)]
    #
    # img_paths = sorted(img_paths, key=lambda i: int(ntpath.basename(i).replace("frame_", "").replace(".jpg", "")))
    # # img_paths = img_paths[::-1]
    # EdgeTracker(threading.Thread).run(paths=img_paths)

import cv2
import numpy as np


class DiffFrame(object):
    def __init__(self, is_first, thresh):
        self.is_first = is_first
        self.thresh = thresh
        self.open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def detect(self, origin_img):
        if self.is_first:
            first_img = origin_img.copy()
            gray_img_old = cv2.cvtColor(first_img, cv2.COLOR_BGR2GRAY)
            self.guass_img_old = cv2.GaussianBlur(gray_img_old, (3, 3), 0)
            self.is_first = False
        else:
            gray_img_new = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)
            guass_img_new = cv2.GaussianBlur(gray_img_new, (3, 3), 0)
            ## opencv diff API
            diff_img = cv2.absdiff(guass_img_new, self.guass_img_old)
            thresh_img = cv2.threshold(diff_img, self.thresh, 255, cv2.THRESH_BINARY)
            opening_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, self.open_kernel)
            conturs = cv2.findContours(opening_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

            for cnt in conturs:
                perimeter = cv2.arcLength(cnt, True)
                if int(perimeter) > 500:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(origin_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            self.guass_img_old = guass_img_new.copy()
        return origin_img

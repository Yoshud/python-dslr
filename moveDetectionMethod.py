from init_methods import *
import imutils
import copy


def to_gray(frame):
    opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, None)
    gray = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)
    return gray


def move_detection(gray_last_frame, actual_frame):
    detection = 0
    gray = to_gray(actual_frame)
    frame_to_print = copy.deepcopy(actual_frame)

    delta = cv2.absdiff(gray_last_frame, gray)
    thresh = cv2.threshold(delta, 20, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("adam", thresh)

    rect = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    thresh = cv2.dilate(thresh, rect, iterations=1)
    # cv2.imshow("adam3", thresh)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    cnts_count = 0
    too_big_count = False
    for c in cnts:
        if cv2.contourArea(c) < 2000:
            continue
        if cv2.contourArea(c) > 200000:
            too_big_count = True

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame_to_print, (x, y), (x + w, y + h), (0, 255, 0), 2)
        detection = 1
        cnts_count += 1

    if cnts_count > 9 or too_big_count:
        detection = 2

    return detection, gray, frame_to_print

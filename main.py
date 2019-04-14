from init_methods import *
import imutils


def to_gray(frame):
    opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, None)
    gray = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)
    return gray


camera, context = init()
last_frame = to_gray(capture_frame(camera, context))

try:
    for i in range(300):
        frame = capture_frame(camera, context)
        gray = to_gray(frame)
        delta = cv2.absdiff(last_frame, gray)
        thresh = cv2.threshold(delta, 20, 255, cv2.THRESH_BINARY)[1]

        cv2.imshow("adam", thresh)

        rect = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        thresh = cv2.dilate(thresh, rect, iterations=1)
        cv2.imshow("adam3", thresh)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        cntsCount = 0
        tooBigCount = False
        for c in cnts:
            if cv2.contourArea(c) < 2000:
                continue
            if cv2.contourArea(c) > 200000:
                tooBigCount = True

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cntsCount += 1

        if cntsCount > 10 or tooBigCount:
            print(f"camera move {i}")

        cv2.imshow("adam2", frame)

        last_frame = gray

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    print("stop")
    cv2.destroyAllWindows()
    error = gp.gp_camera_exit(camera, context)

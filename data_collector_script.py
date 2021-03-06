import os
import sys
import datetime
from move_detection_methods import *

FRAMES_OMITTED_AFTER_CAMERA_MOVE_DETECTED = 5
FRAMES_SAVED_AFTER_LAST_MOVE_DETECTED = 2

camera, context = init()
print(sys.argv)
if len(sys.argv) > 1:
    directoryName = sys.argv[1]
    if os.path.isdir(directoryName):
        directoryName = f"{directoryName}_{datetime.datetime.now()}"
else:
    directoryName = f"recording_{datetime.datetime.now()}"
os.mkdir(directoryName)

last_frame_raw = capture_frame(camera, context)
last_frame = to_gray(last_frame_raw)
last_detection = -1
cameraMovedBreakCounter = 0
afterMoveDetectionCounter = 0

savedCount = 0
i = 0
try:
    while 1:
        frame = capture_frame(camera, context)
        detection, gray, to_print_frame = move_detection(last_frame, frame)

        if detection == 0:
            text = "No move"
        elif detection == 1:
            text = "Move detected!"
        elif detection == 2:
            text = "Camera moved!"
        else:
            text = "Undefined error"

        if cameraMovedBreakCounter == 0:
            if detection == 1:
                cv2.imwrite(f"{directoryName}/frame_{i}.png", frame)
                savedCount += 1
                afterMoveDetectionCounter = FRAMES_SAVED_AFTER_LAST_MOVE_DETECTED
            elif detection != 2 and afterMoveDetectionCounter != 0:
                cv2.imwrite(f"{directoryName}/frame_{i}.png", frame)
                savedCount += 1
                afterMoveDetectionCounter -= 1
            else:
                afterMoveDetectionCounter = 0

            if last_detection == 0 and detection == 1:
                cv2.imwrite(f"{directoryName}/frame_{i-1}.png", last_frame_raw)
                savedCount += 1
        else:
            cameraMovedBreakCounter -= 1

        if detection == 2:
            cameraMovedBreakCounter = FRAMES_OMITTED_AFTER_CAMERA_MOVE_DETECTED
            afterMoveDetectionCounter = 0

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(to_print_frame, f"frame_{savedCount}_{i}", (50, 650), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(to_print_frame, f"saved: {savedCount}", (800, 650), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(to_print_frame, text, (50, 620), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow(f"frame", to_print_frame)

        if cv2.waitKey(10) & 0xFF in [27, ord('q')]:
            break

        i += 1
        last_frame = gray
        last_frame_raw = frame
        last_detection = detection

finally:
    print("stop")
    cv2.destroyAllWindows()
    error = gp.gp_camera_exit(camera, context)

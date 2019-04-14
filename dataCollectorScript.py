import os
import sys
import datetime
from moveDetectionMethod import *

camera, context = init()
print(sys.argv)
if len(sys.argv) > 1:
    directoryName = sys.argv[1]
    if os.path.isdir(directoryName):
        directoryName = f"{directoryName}_{datetime.datetime.now()}"
else:
    directoryName = f"recording_{datetime.datetime.now()}"
os.mkdir(directoryName)

last_frame = to_gray(capture_frame(camera, context))

i = 0
try:
    while 1:
        frame = capture_frame(camera, context)
        detection, gray, to_print_frame = move_detection(last_frame, frame)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.imwrite(f"{directoryName}/frame_{i}.png", frame)
        cv2.putText(to_print_frame, f"frame_{i}", (50, 650), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

        if detection == 0:
            text = "No move"
        elif detection == 1:
            text = "Move detected!"
        elif detection == 2:
            text = "Camera moved!"
        else:
            text = "Undefined error"

        cv2.putText(to_print_frame, text, (50, 620), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow(f"frame", to_print_frame)

        if cv2.waitKey(10) & 0xFF in [27, ord('q')]:
            break

        i += 1
        last_frame = gray

finally:
    print("stop")
    cv2.destroyAllWindows()
    error = gp.gp_camera_exit(camera, context)

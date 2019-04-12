from init_methods import *
import os
import sys
import datetime

camera, context = init()
print(sys.argv)
if len(sys.argv) > 1:
    directoryName = sys.argv[1]
    if os.path.isdir(directoryName):
        directoryName = f"{directoryName}_{datetime.datetime.now()}"
else:
    directoryName = f"recording_{datetime.datetime.now()}"
os.mkdir(directoryName)

gp.gp_camera_capture(camera, 0, context)
i = 0
try:
    while 1:
        frame = capture_photo(camera, context)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.imwrite(f"{directoryName}/frame_{i}.png", frame)
        cv2.putText(frame, f"frame_{i}", (50, 650), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow(f"frame", frame)

        if cv2.waitKey(10) & 0xFF in [27, ord('q')]:
            break
        i += 1

finally:
    print("stop")
    cv2.destroyAllWindows()
    error = gp.gp_camera_exit(camera, context)

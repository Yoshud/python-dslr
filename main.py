from init_methods import *

camera, context = init()
last_frame = capture_photo(camera, context)

try:
    for i in range(300):
        photo = capture_photo(camera, context)
        cv2.imshow("adam", (255 - cv2.cvtColor(last_frame, cv2.COLOR_RGB2GRAY)) - (
                    255 - cv2.cvtColor(photo, cv2.COLOR_RGB2GRAY)))
        # cv2.imshow("adam", photo)
        # cv2.imshow("adam", (255 - last_frame))

        last_frame = photo

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    print("stop")
    cv2.destroyAllWindows()
    error = gp.gp_camera_exit(camera, context)

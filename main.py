from init_methods import *

camera, context = init()
last_frame = capture_photo(camera, context)

try:
    for i in range(300):
        photo = capture_photo(camera, context)
        # # photo = cv2.flip(photo, 1)
        cv2.imshow("adam", (255 - last_frame) - (255 - photo))
        # cv2.imshow("adam", (255 - last_frame))

        last_frame = photo

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    print("stop")
    cv2.destroyAllWindows()
    error = gp.gp_camera_exit(camera, context)


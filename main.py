import cv2
# import piggyphoto
# import pygame
import gphoto2 as gp


# def show(file):
#     picture = pygame.image.load(file)
#     main_surface.blit(picture, (0, 0))
#     pygame.display.flip()
#
#
# camera = gp.gp_camera_new(camera)
# C = piggyphoto.camera()
# C.leave_locked()
# C.capture_preview('p.jpg')
# img = cv.imread('p.jpg')
# img

context = gp.gp_context_new()
error, file = gp.gp_file_new()
error, camera = gp.gp_camera_new()
error = gp.gp_camera_init(camera, context)
error, text = gp.gp_camera_get_summary(camera, context)
error, file = gp.gp_camera_capture_preview(camera, context)
gp.gp_file_save(file, "photo.jpg")
print('Summary')
print('=======')
print(text.text)
# error = gp.gp_camera_trigger_capture(camera, context)
# error, filePath = gp.gp_camera_capture(camera, 1, context)
print(gp.gp_result_as_string(error))
# gp.gp_camera_file_get()

print("start")
try:
    for i in range(300):
        error, file = gp.gp_camera_capture_preview(camera, context)
        # error, filePath = gp.gp_camera_capture(camera, 0, context)
        print(gp.gp_result_as_string(error))
        gp.gp_file_save(file, "photo.jpg")
        photo = cv2.imread("photo.jpg")
        # # photo = cv2.flip(photo, 1)
        cv2.imshow("adam", photo)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    print("stop")
    cv2.destroyAllWindows()
    error = gp.gp_camera_exit(camera, context)

# picture = pygame.image.load("p.jpg")
# pygame.display.set_mode(picture.get_size())
# main_surface = pygame.display.get_surface()
#
# while True:
#     C.capture_preview('p.jpg')
#     show("p.jpg")

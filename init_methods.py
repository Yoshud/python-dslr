import cv2
import gphoto2 as gp

def capture_photo(camera, context):
    error, file = gp.gp_camera_capture_preview(camera, context)
    print(gp.gp_result_as_string(error))
    gp.gp_file_save(file, "photo.jpg")
    photo = cv2.imread("photo.jpg")
    return photo

def init():
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
    print(gp.gp_result_as_string(error))

    print("start")
    return camera, context
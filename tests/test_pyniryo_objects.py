

def detect_color_objects_using_nyro(image):
    from utils import get_undistorted_img_from_camera, detect_color_objects_using_nyro
    import cv2

    # Load a test image (replace 'test_image.jpg' with your image path)
    img_test = cv2.imread('test_image.jpg')
    if img_test is None:
        raise FileNotFoundError("Test image not found. Please provide a valid image path.")

    # Detect color objects
objects = detect_color_objects_using_nyro(img_test)
for center, angle in objects:
    print("Object center:", center, "angle:", angle)

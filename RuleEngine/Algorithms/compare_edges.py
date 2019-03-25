import cv2
import numpy as np

def calculate_canny_edges(image_a, image_b):
    """ This function performs a canny edge detection on two given images, afterwards the edges are compared
    :param image_a OpenCV Image,
    :param image_b OpenCV Image
    :returns A factor 0.0 up to 1.0 of as a percentage of how much the images differ
    If a result of inf is returned this indicates that the check could not be run. """
    # Todo: Create Input with different color scheme but same regions
    # ToDo: Check kernel configuration that it may depend on the image size
    kernel = np.ones((5, 5), np.uint8)

    gray_image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    # ToDo: Improve calculation of thresholds
    edges_a = cv2.Canny(gray_image_a, 30, 30*3)
    edges_b = cv2.Canny(gray_image_b, 30, 30*3)


    # Lets dilate the output to fill holes and to alleviate the issue that some lines may only slightly diverge
    edges_a = cv2.dilate(edges_a, kernel)
    edges_b = cv2.dilate(edges_b, kernel)


    if edges_a.size == edges_b.size:
        diff = edges_a - edges_b
        # 1 is equal to 255 (white dot)
        different_pixels = diff.sum() / 255
        total_pixels = diff.size
        percent_difference = different_pixels / total_pixels

        # print('Amount of % difference ' + str(percent_difference * 100) + ' %')
        # cv2.imshow('grad', diff)
        # cv2.waitKey(0)

        result = percent_difference, diff
    else:
        result = float('inf'), '0'

    return result


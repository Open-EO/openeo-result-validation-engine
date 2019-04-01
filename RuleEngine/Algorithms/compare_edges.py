import cv2
import numpy as np


def calculate_canny_edges(image_a, image_b, combination, threshold):
    """ This function performs a canny edge detection on two given images, afterwards the edges are compared
    :param image_a OpenCV Image,
    :param image_b OpenCV Image
    :returns A factor 0.0 up to 1.0 of as a percentage of how much the images differ
    If a result of inf is returned this indicates that the check could not be run.
    ref: https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/ """
    # Todo: Create Input with different color scheme but same regions
    kernel = np.ones((5, 5), np.uint8)

    gray_image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    # compute the median of the single channel pixel intensities
    v = np.median(gray_image_a)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))

    # compute the median of the single channel pixel intensities
    v_b = np.median(gray_image_b)
    # apply automatic Canny edge detection using the computed median
    lower_b = int(max(0, (1.0 - 0.33) * v_b))
    upper_b = int(min(255, (1.0 + 0.33) * v_b))

    edges_a = cv2.Canny(gray_image_a, lower, upper)
    edges_b = cv2.Canny(gray_image_b, lower_b, upper_b)

    #edges_a = cv2.dilate(edges_a, kernel)
    #edges_b = cv2.dilate(edges_b, kernel)

    result = {}

    if edges_a.size == edges_b.size:
        diff = edges_a - edges_b
        # diff = cv2.dilate(diff, kernel)

        # diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
        # diff = cv2.erode(diff, np.ones((5, 5), np.uint8))

        #cv2.imshow('edges_a', edges_a)
        #cv2.imshow('edges_b', edges_b)
        #cv2.imshow('diff', diff)
        #cv2.waitKey(0)
        # 1 is equal to 255 (white dot)
        different_pixels = diff.sum() / 255
        total_pixels = diff.size
        percent_difference = different_pixels / total_pixels

        result['percent_diff'] = percent_difference
        if percent_difference < float(threshold):
            result['Edge-diff'] = ['passed', str(percent_difference)]
        else:
            result['Edge-diff'] = ['failed', str(percent_difference)]
            # When the rule failed: save difference image
            combination = ((combination[0].strip('.png')).strip('.jpg') +
                           '_' + (combination[1].strip('.png')).strip('.jpg')).replace('/', '_')
            combination = 'reports/EDGE' + combination + '.png'
            difference_image = (diff * 255).astype("uint8")
            cv2.imwrite(combination, difference_image)
            result['edge-image-path'] = combination

    else:
        result['percent_diff'] = 'Test was not able to run due to different image sizes'

    return result


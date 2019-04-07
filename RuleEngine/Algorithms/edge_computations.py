import cv2
import numpy as np


def calculate_canny_edges(image_a, image_b):
    """ This function performs a canny edge detection on two given images, afterwards the edges are compared
    :param image_a OpenCV Image,
    :param image_b OpenCV Image,
    :returns A dict with a factor 0.0 up to 1.0 of as a percentage of how much the images differ and the image of the edges
    ref: https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/ """
    images = [image_a, image_b]
    edge_images = []
    for image in images:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # compute the median of the single channel pixel intensities
        v = np.median(gray_image)
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - 0.33) * v))
        upper = int(min(255, (1.0 + 0.33) * v))
        # apply automatic Canny edge detection using the computed median
        edges = cv2.Canny(gray_image, lower, upper)
        edge_images.append(edges)

    return edge_images


def compute_overlap(edge_images):
    if edge_images[0].size == edge_images[1].size:
        # Overlap computation
        # ToDo: Work out proper calculation
        # ref: http://answers.opencv.org/question/37392/how-to-compute-intersections-of-two-contours/
        # the higher the overlap the better
        height, width = edge_images[0].shape
        overlap_image = np.zeros((height, width), np.uint8)
        cv2.bitwise_and(edge_images[0], edge_images[1], overlap_image)
        # sum of all edges
        non_zero_image_a = cv2.countNonZero(edge_images[0])
        #non_zero_image_b = cv2.countNonZero(edge_images[1])
        # sum of the overlap (should be lower than the sums)
        non_zero_overlap_image = cv2.countNonZero(overlap_image)
        percent_difference_roi_a = non_zero_overlap_image / non_zero_image_a
        #percent_difference_roi_b = non_zero_overlap_image / non_zero_image_b
        return percent_difference_roi_a
    else:
        return None


def create_comparison_image(edge_images):
    if edge_images[0].size == edge_images[1].size:
        height, width = edge_images[0].shape
        overlap_image_a = np.zeros((height, width, 3), np.uint8)
        overlap_image_b = np.zeros((height, width, 3), np.uint8)
        contours, _ = cv2.findContours(edge_images[0], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours_b, _ = cv2.findContours(edge_images[1], cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # Draw the contours red for image_a
        cv2.drawContours(overlap_image_a, contours, -1, (0, 0, 255), 3)
        # Draw the contours green for image_b
        cv2.drawContours(overlap_image_b, contours_b, -1, (0, 255, 0), 3)
        comparison_image = overlap_image_a + overlap_image_b
        return comparison_image
    else:
        return None


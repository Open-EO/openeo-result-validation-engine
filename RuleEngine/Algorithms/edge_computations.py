import cv2
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def calculate_canny_edges(image_a, image_b, align_images):
    """ This function performs a canny edge detection on two given images, afterwards the edges are compared
    :param image_a OpenCV Image,
    :param image_b OpenCV Image,
    :param align_images boolean, whether the images should be aligned with image registration
    :returns an array of an image pair, where canny edge detection was performed on
    ref: https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    """
    # We translate the image_a to fit to image_b
    # if image_a.shape == image_b.shape and align_images == True:
    #     image_a, homography = img_registration(image_a, image_b)
    images = [image_a, image_b]
    edge_images = []
    for image in images:
        try:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # This should not be caught with an exception :)
        except cv2.error:
            scaler = MinMaxScaler(copy=False, feature_range=(0, 255))
            scaler.fit_transform(image)
            gray_image = np.uint8(image)

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
    """ Returns the overlap of two binary images """
    if edge_images[0].size == edge_images[1].size:
        # Overlap computation
        # ref: http://answers.opencv.org/question/37392/how-to-compute-intersections-of-two-contours/
        height, width = edge_images[0].shape
        sum_images = np.zeros((height, width), np.uint8)
        overlap_image = np.zeros((height, width), np.uint8)

        cv2.bitwise_and(edge_images[0], edge_images[1], overlap_image)
        cv2.bitwise_or(edge_images[0], edge_images[1], sum_images)
        non_zero_overlap_image = cv2.countNonZero(overlap_image)
        non_zero_sum_image = cv2.countNonZero(sum_images)

        try:
            overlap_percentage = non_zero_overlap_image / non_zero_sum_image
            return overlap_percentage

        except ZeroDivisionError:
            return 0.0
    else:
        return None


def create_comparison_image(edge_images):
    """ creates an comparison image, this image has yellow lines for overlap,
    red and green for the edges that do not overlap"""
    if edge_images[0].size == edge_images[1].size:
        height, width = edge_images[0].shape
        overlap_image_a = np.zeros((height, width, 3), np.uint8)
        overlap_image_b = np.zeros((height, width, 3), np.uint8)
        contours, _ = cv2.findContours(edge_images[0], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_b, _ = cv2.findContours(edge_images[1], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # We could also only compare the n largest contours
        # cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        # cnts_b = sorted(contours_b, key=cv2.contourArea, reverse=True)[:10]
        # Draw the contours red for image_aw
        cv2.drawContours(overlap_image_a, contours, -1, (0, 0, 255), 3)
        # Draw the contours green for image_b
        cv2.drawContours(overlap_image_b, contours_b, -1, (0, 255, 0), 3)
        comparison_image = overlap_image_a + overlap_image_b
        return comparison_image
    else:
        return None


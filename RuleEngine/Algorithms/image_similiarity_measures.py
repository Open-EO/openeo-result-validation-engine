import logging

import cv2
import numpy as np
from skimage.measure import compare_ssim, compare_mse, compare_nrmse, compare_psnr


def image_similarity_measures(image_a, image_b):
    logger = logging.getLogger(__name__)

    result = {}

    # Align image_a to image_b
    image_a, homography = img_registration(image_a, image_b)

    functions = [compare_mse, compare_nrmse, compare_psnr, compare_ssim]
    difference_image = None

    for function in functions:
        logger.info('Executing {}'.format(function.__name__))

        if function.__name__ == 'compare_ssim':
            gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
            gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
            score, difference_image = function(gray_a, gray_b, full=True)
            if score != 1.0:
                difference_image = (difference_image * 255).astype("uint8")
            result[function.__name__] = score
        else:
            score = function(image_a, image_b)
            if score == float("inf"):
                score = "infinity"
            result[function.__name__] = score

    return result, difference_image


def img_registration(image_a, image_b):
    # https://www.learnopencv.com/image-alignment-feature-based-using-opencv-c-python/
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(500)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * 0.25)
    matches = matches[:numGoodMatches]

    # Draw top matches
    #imMatches = cv2.drawMatches(image_a, keypoints1, image_b, keypoints2, matches, None)
    #cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = image_b.shape
    imbReg = cv2.warpPerspective(image_a, h, (width, height))
    return imbReg, h

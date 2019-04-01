import cv2
import logging
from skimage.measure import compare_ssim, compare_mse, compare_nrmse, compare_psnr


def image_similarity_measures(image_a, image_b, combination_name, threshold):
    logger = logging.getLogger(__name__)

    check = 'passed'
    result = {}

    functions = [compare_mse, compare_nrmse, compare_psnr, compare_ssim]

    for function in functions:
        logger.info('Executing {}'.format(function.__name__))

        if function.__name__ == 'compare_ssim':
            gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
            gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
            score, difference_image = function(gray_a, gray_b, full=True)
            if score != 1.0:
                difference_image = (difference_image * 255).astype("uint8")
                cv2.imwrite(combination_name + '.png', difference_image)
                result['differenceImage_Path'] = combination_name + '.png'
            result[function.__name__] = score
        else:
            score = function(image_a, image_b)
            result[function.__name__] = score

        # ToDo: Weigh the score with the threshold and judge whether the test passed or not
        # ToDo: Create map of functions and what their return value means
        if score in [0.0, 1.0, float("inf")]:
            check = 'passed'
        else:
            check = 'failed'

    result['rule'] = check
    return result


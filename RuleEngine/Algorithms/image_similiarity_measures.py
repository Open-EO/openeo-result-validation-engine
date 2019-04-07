import logging

import cv2
from skimage.measure import compare_ssim, compare_mse, compare_nrmse, compare_psnr


def image_similarity_measures(image_a, image_b, file_save_path):
    logger = logging.getLogger(__name__)

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
                file_save_path = 'reports/SSIM' + file_save_path + '.png'
                cv2.imwrite(file_save_path, difference_image)
                result['differenceImage_Path'] = file_save_path
            result[function.__name__] = score
        else:
            score = function(image_a, image_b)
            if score == float("inf"):
                score = "infinity"
            result[function.__name__] = score

    return result


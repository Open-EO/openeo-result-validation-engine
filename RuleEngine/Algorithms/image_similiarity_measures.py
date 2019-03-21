from skimage.measure import compare_ssim, compare_mse, compare_nrmse, compare_psnr
import cv2


def run_image_similarity_measures(image_a, image_b, threshold):
    scores = []
    result = 'passed'
    difference_image = []

    functions = [compare_mse, compare_nrmse, compare_psnr, compare_ssim]

    for function in functions:
        # ToDo: Find better solution to execute structural similarity index
        if function.__name__ == 'compare_ssim':
            gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
            gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
            score, difference_image = function(gray_a, gray_b, full=True)
        else:
            score = function(image_a, image_b)

        # ToDo: Weigh the score with the threshold and judge whether the test passed or not
        # ToDo: Create map of functions and what their return value means
        if score in [0.0, 1.0, float("inf")]:
            result = 'passed'
        else:
            result = 'failed'
        scores.append((str(function.__name__), score))

    return scores, result, difference_image


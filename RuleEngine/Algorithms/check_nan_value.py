import numpy as np


def check_nan_value(image_a, image_b):
    result_image_a = check_single_image_nan(image_a)
    result_image_b = check_single_image_nan(image_b)

    if result_image_a and result_image_b:
        result = {
            'file_provider': result_image_a,
            'file_compared': result_image_b
        }
    else:
        result = None

    return result


def check_single_image_nan(image):
    zero_in_image = 0 in image
    nan_in_image = np.isnan(image).any()

    if zero_in_image and nan_in_image:
        result = {
            'types': [0, str(np.nan)],
            'amount': np.count_nonzero(image == 0) + np.count_nonzero(np.isnan(image))
        }
    elif zero_in_image and not nan_in_image:
        result = {
            'types': [0],
            'amount': np.count_nonzero(image == 0)
        }
    elif nan_in_image:
        result = {
            'types': [str(np.nan)],
            'amount': np.count_nonzero(np.isnan(image))
        }
    else:
        result = {
            'amount': 0
        }
    return result

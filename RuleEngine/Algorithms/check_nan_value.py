import numpy as np


def check_nan_value(image):
    zero_in_image = 0 in image
    nan_in_image = np.isnan(image).any()
    result = {}

    if zero_in_image and nan_in_image:
        result['types'] = [0, np.nan]
        result['amount'] = np.count_nonzero(image == 0) + np.count_nonzero(np.isnan(image))
        return result
    elif zero_in_image and not nan_in_image:
        result['types'] = [0]
        result['amount'] = np.count_nonzero(image == 0)
        return result
    elif nan_in_image:
        result['types'] = [np.nan]
        result['amount'] = np.count_nonzero(np.isnan(image))
        return result

    return None

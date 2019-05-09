import numpy as np


def check_nan_value(image_a, image_b):
    result_image_a = check_single_image_nan(image_a)
    result_image_b = check_single_image_nan(image_b)

    if result_image_a and result_image_b:
        result = {
            'file_' + 'a': result_image_a,
            'file_' + 'b': result_image_b
        }
    else:
        result = None

    return result


def check_single_image_nan(image):
    # ToDo: This NaN Check does not work properly for images as NaN values do not exist
    #  they are transparent RGBA(R, G, B, 0), white is RGB(255,255,255)
    white_in_image = [255, 255, 255] in image
    nan_in_image = np.isnan(image).any()

    if white_in_image and nan_in_image:
        result = {
            'types': ['white', 'transparent'],
            'count': [np.count_nonzero(image == [255, 255, 255]), np.count_nonzero(np.isnan(image))]
        }
    elif white_in_image and not nan_in_image:
        result = {
            'types': ['white'],
            'count': np.count_nonzero(image == [255, 255, 255])
        }
    elif nan_in_image:
        result = {
            'types': ['transparent'],
            'count': np.count_nonzero(np.isnan(image))
        }
    else:
        result = {
            'count': 0
        }
    return result

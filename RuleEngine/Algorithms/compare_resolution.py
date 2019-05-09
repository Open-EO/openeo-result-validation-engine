from numpy import divide
import numpy as np


def compare_resolution(image_a, image_b):
    """ This is a check that can be used to prevent errors (image similarity algorithms require that
    the input size is equal and also to maybe give information if the resolution is smaller or greater than expected
    :returns a tuple of factors for the difference between width, height and the bands"""
    # We need to pad the shape if the image has a different amount of bands
    max_length = max(len(image_a.shape), len(image_b.shape))
    min_length = min(len(image_a.shape), len(image_b.shape))
    pad_length = max_length - min_length

    # only pad the shorter one
    if image_a.shape < image_b.shape:
        image_a_shape = np.pad(image_a.shape, (0, pad_length), mode='constant')
        image_b_shape = image_b.shape
    else:
        image_a_shape = image_a.shape
        image_b_shape = np.pad(image_b.shape, (0, pad_length), mode='constant')

    try:
        factors = divide(image_a_shape, image_b_shape)

        factors_list = [factor for factor in factors]
    except ValueError:
        factors_list = None

    return {'resolution_factors': factors_list,
            'desription': 'Image a is X times smaller/greater than image b'}

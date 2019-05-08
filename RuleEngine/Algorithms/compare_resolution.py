from numpy import divide


def compare_resolution(image_a, image_b):
    """ This is a check that can be used to prevent errors (image similarity algorithms require that
    the input size is equal and also to maybe give information if the resolution is smaller or greater than expected
    :returns a tuple of factors for the difference between width, height and the bands"""
    try:
        factors = divide(image_a.shape, image_b.shape)
        factors_list = [factor for factor in factors]
    except ValueError:
        factors_list = None

    return {'resolution_factors': factors_list,
            'desription': 'Image a is X times smaller/greater than image b'}

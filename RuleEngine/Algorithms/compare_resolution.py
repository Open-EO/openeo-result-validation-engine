from numpy import divide


def compare_resolution(image_a, image_b):
    """ This is a check that can be used to prevent errors (image similarity algorithms require that
    the input size is equal and also to maybe give information if the resolution is smaller or greater than expected
    :returns a tuple of factors for the difference between width, height and the bands"""
    try:
        width_factor, height_factor, bands_factor = divide(image_a.shape, image_b.shape)
    except ValueError:
        # ToDo: Think about whether the function should return infinite values or some error message
        width_factor, height_factor, bands_factor = (None, None, None)

    return {'widthFactor': width_factor,
            'heightFactor': height_factor,
            'bandsFactor': bands_factor}

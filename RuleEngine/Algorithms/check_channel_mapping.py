
def check_channel_mapping(image_a, image_b):
    """ Receives two input images and checks their band mapping"""
    # ToDo: This implementation is not correct, write a function that compares two images and checks
    #  whether they might be inverted
    mixed_bands = False
    # If the images are not equal, check the channel mapping as they might be mixed up
    if image_a.all() != image_b.all():
        if image_a[0].all() == image_b[1].all():
            print('Band 0 is switched with Band 1')
            mixed_bands = True

        if image_a[1].all() == image_b[2].all():
            print('Band 1 is switched with Band 2')
            mixed_bands = True
        if image_a[2].all() == image_b[0].all():
            print('Band 2 is switched with Band 0')
            mixed_bands = True
        return mixed_bands
    else:
        return mixed_bands

from itertools import product

def check_channel_mapping(image_a, image_b):
    """ Receives two input images and checks their band mapping"""
    # ToDo: This implementation is not correct, write a function that compares two images and checks
    #  whether they might be inverted
    bands = [0, 1, 2]
    combis = product(bands, bands)
    # If the images are not equal, check the channel mapping as they might be mixed up
    if image_a.shape == image_b.shape:
        for combi in combis:
            #print(combi)
            #print('is channel ' + str(combi[0]) + ' equal to channel ' + str(combi[1]) + '?')
            #print(np.array_equal(image_a[combi[0]], image_b[combi[1]]))
            continue

    return None

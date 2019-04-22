import os


def compare_filesize(image_path_a, image_path_b):
    """ Compares the file size of a file A with file B
    :returns file sizes and factor """
    file_size_a = os.stat(image_path_a).st_size
    file_size_b = os.stat(image_path_b).st_size
    result = {
        'file_size_a': file_size_a,
        'file_size_b': file_size_b
        'file_size_factor': file_size_a/file_size_b
    }

    return result

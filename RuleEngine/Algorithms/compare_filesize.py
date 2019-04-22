import os
from hurry.filesize import size
from hurry.filesize import alternative

def compare_filesize(image_path_a, image_path_b):
    """ Compares the file size of a file A with file B
    :returns file sizes and factor """
    file_size_a = os.stat(image_path_a).st_size
    file_size_b = os.stat(image_path_b).st_size

    # Todo: Integrate a better way to get the provider
    result = {
        'file_size_'+image_path_a.split('/')[3]: size(file_size_a, system=alternative),
        'file_size_'+image_path_b.split('/')[3]: size(file_size_b, system=alternative),
        'file_size_factor': file_size_a/file_size_b
    }

    return result

import os


def compare_filesize(file_path, files):
    """ Compares the file size of a given file with the mean file size of all files
    :returns number of the mean deviation in percent """
    # ToDo: Rewrite this to compare two files
    file_sizes = []
    for file in files:
        file_sizes.append(os.stat(file).st_size)

    mean_file_size = sum(file_sizes) / len(file_sizes)

    return os.stat(file_path).st_size / mean_file_size

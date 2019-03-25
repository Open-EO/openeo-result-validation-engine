def compare_filenames(file_a, file_b):

    _, ext_a = file_a.split('.')
    _, ext_b = file_b.split('.')

    equal_extension = True if ext_a == ext_b else False
    # ToDo: Maybe check for identical filenames as some users may expect such behaviour
    return equal_extension

def compare_filenames(file_a, output_format):

    _, ext_a = file_a.split('.')
    #_, ext_b = file_b.split('.')

    ext_a = ext_a.lower()
    #ext_b = ext_b.lower()
    output_format = output_format.lower()

    # equal_extension = True if (ext_a == ext_b) and (ext_a == output_format) else False
    equal_extension = True if ext_a == output_format else False
    # ToDo: Maybe check for identical filenames as some users may expect such behaviour
    return equal_extension

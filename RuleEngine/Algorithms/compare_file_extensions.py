def compare_file_extensions(file_a, output_format):
    _, ext_a = file_a.split('.')
    ext_a = ext_a.lower()
    output_format = output_format.lower()
    equal_extension = True if ext_a == output_format else False
    return equal_extension

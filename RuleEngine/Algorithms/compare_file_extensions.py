def compare_file_extensions(file_a, file_b):
    _, ext_a = file_a.split('.')
    ext_a = ext_a.lower()
    _, ext_b = file_b.split('.')
    ext_b = ext_b.lower()
    equal_extension = True if ext_a == ext_b else False
    return equal_extension

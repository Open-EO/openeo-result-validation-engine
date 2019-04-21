import os
from abc import ABC

import cv2
from skimage.external.tifffile.tifffile import imread as imread_tiff


class Rule(ABC):
    def __init__(self, parameters):
        self._parameters = parameters
        self._name_of_rule
        self._directory = ''
        self._results = []

    def apply(self):
        result = self.check_rule(self._results[0], self._results[1], self._results)
        return result

    def check_rule(self, *kwargs):
        pass

    def set_results(self, results):
        """ Sets the process results i.e the output of the back-ends
         :param results Array with Jsons, one for each file in a job
         Example: {'backend': 'GEE', 'job': 'SWITZERLAND', 'file': 'mock/GEE/Switzerland/86ec0e53-09fb-4436-ac16-09a5df9cead9.png'}
         """
        self._results = results

    def set_directory(self, directory):
        """ Sets the directory path for the report and possible outputs"""
        self._directory = directory

    def get_name_of_rule(self):
        """ This can be used to see which rule is currently processed"""
        return self._name_of_rule

    def create_file_path(self, combination, prepend, ext):
        # Get only the filename
        filename_a = os.path.split(combination[0])[1]
        filename_b = os.path.split(combination[1])[1]
        # Get the filename without extension
        filename_a, _ = os.path.splitext(filename_a)
        filename_b, _ = os.path.splitext(filename_b)
        file_path = self._directory + prepend + (filename_a + '_' + filename_b) + ext
        return file_path

    def read_tiff(self, file_path):
        return imread_tiff(file_path)

    def read_png_jpeg(self, file_path):
        return cv2.imread(file_path)

    def read_image(self, file_path):
        root, ext = os.path.splitext(file_path)
        if ext in ['.tif', '.tiff']:
            return self.read_tiff(file_path)
        else:
            return self.read_png_jpeg(file_path)

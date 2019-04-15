import os

import cv2

from RuleEngine.Algorithms.check_nan_value import check_nan_value
from RuleEngine.Rules.Rule import Rule


class NanValueCheck(Rule):
    def __init__(self, parameters):
        self._files = []
        self._name_of_rule = 'nan-value-check'
        super(NanValueCheck, self).__init__(parameters)

    def apply(self):
        result_arr = []
        for file_path in self._results:
            self._files.append(file_path)
            result_arr.append(self.check_rule(file_path))
        return result_arr

    def check_rule(self, image_path):
        """ Has two image paths as inputs, calls functions that concern the use case of validating classifications """
        image = cv2.imread(image_path)

        result = {'file': os.path.split(image_path)[1]}
        if self._parameters.get('allow-nan', None) is True:
            result['nan-value'] = check_nan_value(image)

        return result

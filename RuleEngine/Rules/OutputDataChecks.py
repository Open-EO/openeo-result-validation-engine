import os

from RuleEngine.Algorithms.compare_file_extensions import compare_file_extensions
from RuleEngine.Algorithms.compare_filesize import compare_filesize
from RuleEngine.Rules.Rule import Rule


class OutputDataChecks(Rule):
    def __init__(self, parameters):
        self._files = []
        self._name_of_rule = 'output-data-checks'
        super(OutputDataChecks, self).__init__(parameters)

    def check_rule(self, image_path_a, image_path_b, combination):
        result = {'combination': combination}
        if self._parameters.get('matching-file-extensions', None) is not None:
            result['matching-file-extensions'] = compare_file_extensions(image_path_a, image_path_b,
                                                                         self._parameters.get('matching-file-extensions'))

        if self._parameters.get('file-size-check') is True:
            result['file-size-check'] = compare_filesize(image_path_a, image_path_b, self._files)

        return result

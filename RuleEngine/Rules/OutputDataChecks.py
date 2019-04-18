import os

from RuleEngine.Algorithms.compare_file_extensions import compare_file_extensions
from RuleEngine.Algorithms.compare_filesize import compare_filesize
from RuleEngine.Rules.Rule import Rule


class OutputDataChecks(Rule):
    def __init__(self, parameters):
        self._files = []
        self._name_of_rule = 'output-data-checks'
        super(OutputDataChecks, self).__init__(parameters)

    def apply(self):
        result_arr = []
        for file_path in self._results:
            self._files.append(file_path)
            result_arr.append(self.check_rule(file_path))
        return result_arr

    def check_rule(self, file_path_a):
        result = {'file': os.path.split(file_path_a)[1] }
        if self._parameters.get('matching-file-extensions', None) is not None:
            result['matching-file-extensions'] = compare_file_extensions(file_path_a,
                                                                         self._parameters.get('matching-file-extensions'))

        # ToDo: Evaluate whether this should also be a comparison between two files
        if self._parameters.get('file-size-check') is True:
            result['file-size-check'] = compare_filesize(file_path_a, self._files)

        return result

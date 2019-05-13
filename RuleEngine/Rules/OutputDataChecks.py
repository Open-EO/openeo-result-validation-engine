from RuleEngine.Algorithms.compare_file_extensions import compare_file_extensions
from RuleEngine.Algorithms.compare_filesize import compare_filesize
from RuleEngine.Rules.Rule import Rule


class OutputDataChecks(Rule):
    def __init__(self, parameters):
        self._files = []
        self._name_of_rule = 'output-data-checks'
        super(OutputDataChecks, self).__init__(parameters)

    def check_rule(self, image_path_a, image_path_b, combination):
        result = {}
        if self._parameters.get('matching-file-extensions', None) is not None:
            result['matching-file-extensions'] = compare_file_extensions(image_path_a, image_path_b)

        if self._parameters.get('file-size-check') is True:
            result['file-size-check'] = compare_filesize(image_path_a, image_path_b)
            file_size_factor = result['file-size-check'].get('file_size_factor')
            if file_size_factor > 1.3 or file_size_factor < 0.8:
                result['file-size-check']['rule'] = 'failed'
            else:
                result['file-size-check']['rule'] = 'passed'

        result['passed'] = str(result['file-size-check']['rule'] == 'passed' and result['matching-file-extensions'])

        return result

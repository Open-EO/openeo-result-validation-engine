from RuleEngine.Algorithms.compare_file_extensions import compare_file_extensions
from RuleEngine.Algorithms.compare_filesize import compare_filesize
from RuleEngine.Rules.Rule import Rule


class OutputDataChecks(Rule):
    def __init__(self, rule_type, parameters, output_format):
        self._output_format = output_format
        super(OutputDataChecks, self).__init__(rule_type, parameters)

    def apply(self):
        result_dict = {}
        for filepath in self._results:
            result_dict[filepath] = self.check_rule(filepath)
        return result_dict

    def check_rule(self, file_path_a):
        result = {}
        if self._parameters['matching-file-extensions']:
            result['matching-file-extensions'] = compare_file_extensions(file_path_a, self._output_format)
        if self._parameters['file-size-check']:
            result['file-size-check'] = compare_filesize(file_path_a, self._results)

        return result

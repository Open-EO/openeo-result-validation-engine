from RuleEngine.Algorithms.compare_filenames import compare_filenames
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

    def check_rule(self, image_path_a):
        result = {}
        if self._parameters['matching-file-extensions']:
            result['matching-file-extensions'] = compare_filenames(image_path_a, self._output_format)
        return result

    # ToDo: Check file size between results

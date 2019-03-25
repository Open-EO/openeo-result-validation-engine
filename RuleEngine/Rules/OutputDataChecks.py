from RuleEngine.Algorithms.compare_filenames import compare_filenames
from RuleEngine.Rules.Rule import Rule


class OutputDataChecks(Rule):
    def __init__(self, rule_type, parameters):
        super(OutputDataChecks, self).__init__(rule_type, parameters)

    def apply(self):
        result_dict = {}
        for combination in self.get_result_combinations():
            combination_result = self.check_rule(combination[0], combination[1])
            result_dict[str(combination)] = combination_result
        return result_dict

    def check_rule(self, image_path_a, image_path_b):
        result = {}
        if self._parameters['identical-filenames']:
            result['identical-filenames'] = compare_filenames(image_path_a, image_path_b)
        return result

    # ToDo: Check file size between results

    # ToDo: Check file extension between results

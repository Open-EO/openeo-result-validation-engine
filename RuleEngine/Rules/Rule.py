from abc import ABC

from itertools import combinations


class Rule(ABC):
    def __init__(self, rule_type, parameters):
        self._ruleType = rule_type
        self._parameters = parameters
        self._passed = False
        self._results = []

    def apply(self):
        result_dict = {}
        for combination in self.get_result_combinations():
            combination_result = self.check_rule(combination[0], combination[1], combination)
            result_dict[str(combination)] = combination_result
        return result_dict

    def check_rule(self, *kwargs):
        pass

    def set_results(self, results):
        """ Sets the process results i.e the output of the back-ends
         :param results Array of file paths """
        self._results = results

    def get_rule_type(self):
        """ This can be used to see which rule is currently processed"""
        return self._ruleType

    def has_passed(self):
        """ This returns the result of the Rule """
        return self._passed

    def get_result_combinations(self):
        """  :returns an array of all (unique) possible combinations of the results i.e the output of the back-ends """
        return set(combinations(self._results, 2))

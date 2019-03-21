from abc import ABC

from itertools import product


class Rule(ABC):
    def __init__(self, rule_type, parameters):
        self.ruleType = rule_type
        self.parameters = parameters
        self.passed = False
        self.results = []

    def apply(self, **kwargs):
        """ Applys the rule on a given object"""
        pass

    def set_results(self, results):
        """ Sets the process results i.e the output of the back-ends
         :param results Array of file paths """
        self.results = results

    def get_rule_type(self):
        """ This can be used to see which rule is currently processed"""
        return self.ruleType

    def has_passed(self):
        """ This returns the result of the Rule """
        return self.passed

    def get_result_combinations(self):
        """  :returns an array of all (unique) possible combinations of the results i.e the output of the back-ends """
        return set(product(self.results, self.results))

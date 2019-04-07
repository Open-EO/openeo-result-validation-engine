import os
from abc import ABC
from itertools import combinations


class Rule(ABC):
    def __init__(self, rule_type, parameters):
        self._ruleType = rule_type
        self._parameters = parameters
        self._directory = ''
        self._results = []

    def apply(self):
        result_arr = []
        for combination in self.get_result_combinations():
            combination_result = self.check_rule(combination[0], combination[1], combination)
            if combination_result:
                combination_result['checked-files'] = [str(combination[0]), str(combination[1])]
            result_arr.append(combination_result)
        return {self._ruleType: result_arr}

    def check_rule(self, *kwargs):
        pass

    def set_results(self, results):
        """ Sets the process results i.e the output of the back-ends
         :param results Array with Jsons, one for each file in a job
         Example: {'backend': 'GEE', 'job': 'SWISS', 'file': 'mock/GEE/Swiss/86ec0e53-09fb-4436-ac16-09a5df9cead9.png'} """
        self._results = results

    def set_directory(self, directory):
        """ Sets the directory path for the report and possible outputs"""
        self._directory = directory

    def get_rule_type(self):
        """ This can be used to see which rule is currently processed"""
        return self._ruleType

    def get_result_combinations(self):
        """  :returns an array of all (unique) possible combinations of the results i.e the output of the back-ends """
        files = []
        for backend_name_file in self._results:
            files.append(backend_name_file['file'])
        return set(combinations(files, 2))

    def create_file_path(self, combination, prepend, ext):
        filename_a = os.path.splitext(combination[0])[0]
        filename_b = os.path.splitext(combination[1])[0]
        file_path = self._directory + prepend + (filename_a + '_' + filename_b).replace('/', '_') + ext
        return file_path

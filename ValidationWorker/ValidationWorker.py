import json
import os
from itertools import combinations


class ValidationWorker:
    def __init__(self, rule_engine, process_results):
        self.processResults = process_results
        self.ruleEngine = rule_engine
        self.directory = ''
        self._report = {}

    def start(self):
        region, job, number = self.processResults[0]['job'].split('-')
        self.directory = os.path.join('reports/', region, job + '-' + number, '')
        # Currently not useful.
        # + str(datetime.datetime.now()) + '/'
        print('Validation of ' + self.processResults[0]['job'] + ' reference job started')
        self.validate()

    def get_result_combinations(self):
        """  :returns an array of all (unique) possible combinations of the results i.e the output of the back-ends """
        files = []
        for backend_name_file in self.processResults:
            files.append(backend_name_file['file'])
        return set(combinations(files, 2))

    def validate(self):
        """ Applies every validation rule on each result combination"""
        for file_combination in self.get_result_combinations():
            # Find out to which provider the file belongs to
            provider_a = self.find_backend(file_combination[0])
            provider_b = self.find_backend(file_combination[1])
            result = {}

            for current_rule in self.ruleEngine.get_rules():
                current_rule.get_name_of_rule
                current_rule.set_results(file_combination)
                current_rule.set_directory(self.directory)
                result_of_rule = current_rule.apply()
                if result_of_rule is not None:
                    result[current_rule.get_name_of_rule()] = result_of_rule

            # Create the key for the provider
            if self._report.get(provider_a) is None:
                self._report[provider_a] = {'results': []}
            if self._report.get(provider_b) is None:
                self._report[provider_b] = {'results': []}

            self._report[provider_a]['results'].append({
                'compared_with': provider_b,
                'file': file_combination[0],
                'compared_against': file_combination[1],
                'rule_result': result
            })
            self._report[provider_b]['results'].append({
                'compared_with': provider_a,
                'file': file_combination[1],
                'compared_against': file_combination[0],
                'rule_result': result
            })

        print('Images and job results analyzed!')
        print('Saving to report to disk')
        self.save_report()

    def save_report(self):
        for provider in self._report.keys():
            path_to_report = os.path.join(self.directory, ('ValidationReport-' + provider + '.json'))
            with open(path_to_report, 'w') as fp:
                json.dump(self._report[provider], fp)

    def find_backend(self, file_name):
        """ Looks up the back end provider for a given file name"""
        for job_info in self.processResults:
            if file_name in job_info['file']:
                return job_info['backend']
        raise Exception('Provider not found')




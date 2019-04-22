import datetime
import json
import os
from itertools import combinations


class ValidationWorker:
    def __init__(self, rule_engine, process_results, backend_providers):
        self.processResults = process_results
        self.ruleEngine = rule_engine
        self.directory = ''
        self._report = {}
        self._backendProviders = backend_providers
        self._report['results'] = []

    def start(self):
        self.directory = 'reports/' + self.processResults[0]['job'] + '/'
        # Currently not useful.
        # + str(datetime.datetime.now()) + '/'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
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
            result = {}
            for current_rule in self.ruleEngine.get_rules():
                current_rule.set_results(file_combination)
                current_rule.set_directory(self.directory)
                result[current_rule.get_name_of_rule()] = current_rule.apply()

            name_of_combination = self.name_of_combination(file_combination)
            self._report['results'].append({name_of_combination: result})

        print('Images and job results analyzed!')
        print('Saving to report to disk')
        self.wrap_report()

    def wrap_report(self):
        analysed_report = {}
        for image_combination in self._report.get('results'):
            for key, results in image_combination.items():
                for job_info in self.processResults:
                    if analysed_report.get(job_info['backend']) is None:
                        analysed_report[job_info['backend']] = {}

                    # We look for the provider and a result that matches to his files
                    if os.path.split(job_info['file'])[1] in key:
                        filename_of_provider = os.path.split(job_info['file'])[1]
                        compared_backend = self.find_backend(key.replace(filename_of_provider, '').strip('__'))
                        if analysed_report.get(job_info['backend']).get(filename_of_provider) is None:
                            analysed_report[job_info['backend']][filename_of_provider] = []
                        analysed_report[job_info['backend']][filename_of_provider].append({
                            'compared_backend': compared_backend,
                            'rule-results': results
                        })

        with open(self.directory + 'ValidationReportByBackend.json', 'w') as fp:
            json.dump(analysed_report, fp)

    def find_backend(self, file_name):
        """ Looks up the back end provider for a given file name"""
        for job_info in self.processResults:
            if file_name in job_info['file']:
                return job_info['backend']
        raise Exception('Provider not found')


    @staticmethod
    def name_of_combination(file_tuple):
        first_file_path = file_tuple[0]
        second_file_path = file_tuple[1]
        first_file = (os.path.split(first_file_path)[1])
        second_file = (os.path.split(second_file_path)[1])
        return first_file + '__' + second_file




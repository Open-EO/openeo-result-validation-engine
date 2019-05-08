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
        print('Validation of ' + self.processResults[0]['job'] + ' reference job started')
        self.validate()

    def get_result_combinations(self):
        """  :returns an array of all (unique) possible combinations of the results i.e the output of the back-ends """
        files = []
        for backend_name_file in self.processResults:
            files.append(backend_name_file['file'])
        return combinations(files, 2)

    def validate(self):
        """ Applies every validation rule on each result combination"""
        for file_combination in self.get_result_combinations():
            # get to Job info for the given file
            # this is currently a work around
            job_info_a = self.find_job_info(file_combination[0])
            job_info_b = self.find_job_info(file_combination[1])

            provider_a = job_info_a['backend']
            provider_b = job_info_b['backend']
            result = {}

            # If both jobs returned results we can validate them against each other, we can still run the validation
            # if the files were previously downloaded
            if (job_info_a['download_successful'] and job_info_b['download_successful']) or \
                    (os.path.exists(file_combination[0]) and os.path.exists(file_combination[1])):
                for current_rule in self.ruleEngine.get_rules():
                    current_rule.get_name_of_rule
                    current_rule.set_results(file_combination)
                    current_rule.set_directory(self.directory)

                    result_of_rule = current_rule.apply()
                    if result_of_rule is not None:
                        result[current_rule.get_name_of_rule()] = result_of_rule
            else:
                result = {
                    'provider_a_download_successful': job_info_a['download_successful'],
                    'provider_b_download_successful': job_info_b['download_successful'],
                    'description': 'Validation could not be performed as atleast one provider did not return data, '
                                   'if there are validation results it is because local results were used'
                }

            result['performance'] = {
                'provider_a': job_info_a['time_to_result'],
                'provider_b': job_info_b['time_to_result'],
                'unit': 'seconds'
            }

            # Create the key for the provider
            if self._report.get(provider_a) is None:
                self._report[provider_a] = {'results': []}
            if self._report.get(provider_b) is None:
                self._report[provider_b] = {'results': []}

            self._report[provider_a]['results'].append({
                'file_a': file_combination[0],
                'file_b': file_combination[1],
                'compared_to_provider': provider_b,
                'results': result
            })
            self._report[provider_b]['results'].append({
                'file_a': file_combination[0],
                'file_b': file_combination[1],
                'compared_to_provider': provider_a,
                'results': result
            })

        print('Images and job results analyzed!')
        print('Saving to report to disk')
        self.save_report()

    def save_report(self):
        for provider in self._report.keys():
            path_to_report = os.path.join(self.directory, ('ValidationReport-' + provider + '.json'))
            with open(path_to_report, 'w') as fp:
                json.dump(self._report[provider], fp)

    def find_job_info(self, file_name):
        """ Looks up the back end provider for a given file name"""
        for job_info in self.processResults:
            if file_name in job_info['file']:
                return job_info
        raise Exception('Job info not found')




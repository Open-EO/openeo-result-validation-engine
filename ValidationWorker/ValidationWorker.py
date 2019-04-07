import datetime
import json
import os


class ValidationWorker:
    def __init__(self, rule_engine, process_results, backend_providers):
        self.processResults = process_results
        self.ruleEngine = rule_engine
        self.directory = ''
        self._report = backend_providers
        self._backendProviders = backend_providers
        self._report['results'] = []

    def start(self):
        self.directory = 'reports/' + self.processResults[0]['job'] + '/' + str(datetime.datetime.now()) + '/'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        print('Validation of ' + self.processResults[0]['job'] + ' reference job started')
        self.validate()

    def validate(self):
        """ Grabs the next validation rule and calls the function with the arguments """
        current_rule = self.ruleEngine.next_rule()
        if current_rule:
            current_rule_name = current_rule.get_rule_type()
            print('Working on: ' + current_rule_name)
            current_rule.set_results(self.processResults)
            current_rule.set_directory(self.directory)

            self._report['results'].append(current_rule.apply())
            self.validate()
        else:
            print('Images and job results analyzed!')
            print('Saving to report to disk')

            with open(self.directory + 'ValidationReport.json', 'w') as fp:
                json.dump(self._report, fp)

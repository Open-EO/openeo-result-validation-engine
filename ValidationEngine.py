import json
import logging

from JobWorker.JobWorker import JobWorker
from RuleEngine.RuleEngine import RuleEngine
from ValidationWorker.ValidationWorker import ValidationWorker

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    with open('backendProvider.json', 'r') as backendProvidersFile:
        backendProviders = json.loads(backendProvidersFile.read())

        jobWorker = JobWorker(backendProviders)
        jobWorker.start_fetching()

        jobs = jobWorker.get_all_jobs()
        for job in jobs:
            with open('default-validation-rules.json', 'r') as default_validation_rules:
                # ToDo: Validation rules should come from job
                default_validation_rules_dict = json.loads(default_validation_rules.read())

                rule_engine = RuleEngine(default_validation_rules_dict)
                rule_engine.parse_rules()

                validation_worker = ValidationWorker(rule_engine, job)
                validation_worker.start()









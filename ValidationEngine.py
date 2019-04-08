import json
import logging

from JobWorker.JobWorker import JobWorker
from RuleEngine.RuleEngine import RuleEngine
from ValidationWorker.ValidationWorker import ValidationWorker

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    with open('min-time.json', 'r') as referenceJob:
        with open('backendProvider.json', 'r') as backendProvidersFile:
            process_graph_with_validation_rules = json.loads(referenceJob.read())
            backendProviders = json.loads(backendProvidersFile.read())

            jobWorker = JobWorker(backendProviders, referenceJob)
            jobWorker.start_fetching()

            jobs = jobWorker.get_all_jobs()
            for job in jobs:
                rule_engine = RuleEngine(process_graph_with_validation_rules)
                rule_engine.parse_rules()

                validation_worker = ValidationWorker(rule_engine, job, backendProviders)
                validation_worker.start()









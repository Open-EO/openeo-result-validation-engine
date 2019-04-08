import json
import logging

from JobWorker.JobWorker import JobWorker
from RuleEngine.RuleEngine import RuleEngine
from ValidationWorker.ValidationWorker import ValidationWorker


def start_processing():
    # ToDO: Rewrite this asap.
    current_job = jobWorker.get_results()
    if current_job:
        # Usually each job would have their own prcoess graph and validation rules
        rule_engine = RuleEngine(process_graph_with_validation_rules)
        rule_engine.parse_rules()

        validation_worker = ValidationWorker(rule_engine, current_job, backendProviders)
        validation_worker.start()
        start_processing()
    else:
        print('Done')


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    with open('min-time.json', 'r') as referenceJob:
        with open('backendProvider.json', 'r') as backendProvidersFile:
            process_graph_with_validation_rules = json.loads(referenceJob.read())
            backendProviders = json.loads(backendProvidersFile.read())

            jobWorker = JobWorker(backendProviders, referenceJob)

            jobWorker.start_fetching()

            start_processing()








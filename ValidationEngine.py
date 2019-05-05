import json
import logging
import os

from JobWorker.JobWorker import JobWorker
from RuleEngine.RuleEngine import RuleEngine
from ValidationWorker.ValidationWorker import ValidationWorker

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(name)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    with open('backendProvider.json', 'r') as backendProvidersFile:
        logger = logging.getLogger('ValidationEngine')
        backendProviders = json.loads(backendProvidersFile.read())

        jobWorker = JobWorker(backendProviders, offline_mode=False)
        jobWorker.start_fetching()

        job_results = jobWorker.get_all_jobs()
        for job_result in job_results:
            # Open the jobs validation rules, this path is saved for every provider
            if os.path.exists(job_result[0]['validation-rules-path']):
                with open(job_result[0]['validation-rules-path'], 'r') as validation_rules:
                    # Defined validation rules
                    validation_rules_dict = json.loads(validation_rules.read())


                # Validation rules selected by name
                if validation_rules_dict.get('ruleset-name') is not None:
                    ruleset_name = validation_rules_dict.get('ruleset-name')
                    logger.info(ruleset_name +' validation rules selected')
                    file_path = os.path.join('rule-configurations', ruleset_name +'-validation-rules.json')
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as rules:
                            validation_rules_dict = json.loads(rules.read())
                    else:
                        logger.warning('Validation rules configuration does not exist, falling back to default rules')
                        with open('rule-configurations/default-validation-rules.json', 'r') as rules:
                            validation_rules_dict = json.loads(rules.read())

                rule_engine = RuleEngine(validation_rules_dict)
                rule_engine.parse_rules()

                validation_worker = ValidationWorker(rule_engine, job_result)
                validation_worker.start()









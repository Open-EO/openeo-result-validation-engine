import json
import logging
import os
import argparse

from JobWorker.JobWorker import JobWorker
from RuleEngine.RuleEngine import RuleEngine
from ValidationWorker.ValidationWorker import ValidationWorker


def read_validation_rules(job_info):
    """Reads the jobs validation rules from the job"""
    logger = logging.getLogger('ValidationRules')
    if os.path.exists(job_info[0]['validation-rules-path']):
        with open(job_info[0]['validation-rules-path'], 'r') as validation_rules:
            # Defined validation rules
            _validation_rules_dict = json.loads(validation_rules.read())

            # Validation rules selected by name
            if _validation_rules_dict.get('ruleset-name') is not None:
                ruleset_name = _validation_rules_dict.get('ruleset-name')
                logger.info(ruleset_name + ' validation rules selected')
                file_path = os.path.join('rule-configurations', ruleset_name + '-validation-rules.json')
                if os.path.exists(file_path):
                    with open(file_path, 'r') as rules:
                        return json.loads(rules.read())
                else:
                    logger.warning(
                        'Validation rules configuration does not exist, falling back to default rules')
                    with open('rule-configurations/default-validation-rules.json', 'r') as rules:
                        return json.loads(rules.read())

            return _validation_rules_dict

    else:
        logger.warning('Validation rules configuration does not exist, falling back to default rules')
        with open('rule-configurations/default-validation-rules.json', 'r') as rules:
            return json.loads(rules.read())


def overwrite_resize_factor(validation_rules, resize_factor):
    """ This function can be used to manually overwrite all resize factors for validation rules """
    for rule in validation_rules['validation']['rules']:
        for key in validation_rules['validation']['rules'][rule]:
            if key == 'resize-factor':
                validation_rules['validation']['rules'][rule]['resize-factor'] = resize_factor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validation Engine')
    parser.add_argument('--offline', default=False, type=bool)
    parser.add_argument('--mock', default=False, type=bool)
    parser.add_argument('--resize', type=float)
    args = vars(parser.parse_args())

    logging.basicConfig(format='%(asctime)s %(name)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    backendProviderFilePath = 'backendProvider.json'
    if args['mock']:
        backendProviderFilePath = 'backendProvider-mock.json'

    with open(backendProviderFilePath, 'r') as backendProvidersFile:
        logger = logging.getLogger('ValidationEngine')
        backendProviders = json.loads(backendProvidersFile.read())

        if args['mock']:
            args['offline'] = True

        jobWorker = JobWorker(backendProviders, offline_mode=args['offline'], mock_mode=args['mock'])
        jobWorker.start_fetching()

        job_results = jobWorker.get_all_jobs()
        for job_result in job_results:
            # Read the validation rules from the job
            validation_rules_dict = read_validation_rules(job_result)
            if args['resize'] and not args['mock']:
                overwrite_resize_factor(validation_rules_dict, args['resize'])
            if args['mock']:
                overwrite_resize_factor(validation_rules_dict, 1)

            # Create configured rules from validation rules
            rule_engine = RuleEngine(validation_rules_dict)
            rule_engine.parse_rules()

            # Pass Rule_
            validation_worker = ValidationWorker(rule_engine, job_result)
            validation_worker.start()











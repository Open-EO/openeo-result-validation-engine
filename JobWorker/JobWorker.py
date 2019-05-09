import os
import time
import json

import openeo
from openeo.auth.auth_bearer import BearerAuth


class JobWorker:
    def __init__(self, backend_providers, offline_mode=None, mock_mode=None, job_identifier_to_run=None):
        self.results = []
        self.offline_mode = offline_mode
        self.selectedJob = job_identifier_to_run
        self.mock_mode = mock_mode
        self.backendProviders = backend_providers
        self._jobs_names = []

    def get_results(self):
        current_job = self.next_job()
        if current_job:
            imagery = []
            for result in self.results:
                if result['job'] == current_job:
                    imagery.append(result)
            return imagery
        else:
            return None

    def next_job(self):
        if self._jobs_names:
            return self._jobs_names.pop()
        else:
            return None

    def get_all_jobs(self):
        jobs = []
        for current_job in self._jobs_names:
            imagery = []
            for result in self.results:
                if result['job'] == current_job:
                    imagery.append(result)
            jobs.append(imagery)
        return jobs

    def start_fetching(self):
        """ This function fetches the results for each backend provider"""
        # ToDo: This should be parallelized, as it sometimes can take long to fetch the results from a provider.
        job_directory = 'openeo-sentinel-reference-jobs/'
        if self.mock_mode:
            job_directory = 'mock-examples'
        # In the future, the regions layer could be removed,
        # it is not factual information but just a pattern for myself
        regions = [f.path for f in os.scandir(job_directory) if f.is_dir()]

        for region in regions:
            jobs = [f.path for f in os.scandir(region) if f.is_dir()]
            for job in jobs:
                for provider in self.backendProviders['providers']:

                    if provider.get('local') is None:
                        user = provider['credentials']['user']
                        password = provider['credentials']['password']

                    process_graph_folder = os.path.join(job, provider['name'])
                    # ToDo: Think whether the directory should contain only one process graph anyway
                    if os.path.exists(process_graph_folder) is False:
                        continue

                    process_graphs = [f for f in os.listdir(process_graph_folder)
                                      if os.path.isfile(os.path.join(process_graph_folder, f))]
                    try:
                        path_to_process_graph = os.path.join(process_graph_folder, process_graphs[0])
                    except Exception:
                        print("Job not configured for provider:", provider)
                        continue
                    path_to_validation_rules = os.path.join(job, 'validation-rules.json')
                    with open(path_to_process_graph, 'r') as process_graph:
                        process_graph = json.loads(process_graph.read())
                        save_path = process_graph_folder.replace(job_directory, 'reports/')

                        if not os.path.exists(save_path):
                            os.makedirs(save_path)

                        job_identifier = region.split('/')[1] + '-' + job.split('/')[-1]
                        # Only run selected job that is passed by the CLI argument
                        if self.selectedJob:
                            if self.selectedJob != job_identifier:
                                continue

                        if provider.get('local') is True:
                            file_path = process_graph['file']
                        else:
                            file_path = save_path + '/' + job_identifier + '.' + 'png'

                        download_successful = False
                        start_time = time.time()
                        time.clock()
                        if self.offline_mode is not True:
                            try:
                                con = openeo.connect(provider['baseURL'], auth_type=BearerAuth,
                                                     auth_options={"username": user, "password": password})
                            except Exception as e:
                                # ToDo: Log if a connection to a provider fails
                                print(e)
                                print('Connection to provider failed')
                                download_successful = False
                            # stopwatch starting
                            if provider['name'] == 'EURAC':
                                try:
                                    print('Downloading synchronously')
                                    con.download(process_graph, 0, file_path, {'format': 'PNG'})
                                    download_successful = True
                                except Exception as e:
                                    print(e)
                                    # ToDo: Log if a result cannot be downloaded and store it in results
                                    download_successful = False
                            else:
                                try:
                                    openEO_job = con.create_job(process_graph, output_format='PNG')
                                    openEO_job.start_job()
                                    print(openEO_job.describe_job())
                                    while download_successful is not True:
                                        try:
                                            openEO_job.download_results(file_path)
                                            download_successful = True
                                        except ConnectionAbortedError:
                                            download_successful = False
                                            print('Retrying to download file in 15 seconds')
                                            print(openEO_job.describe_job())
                                            time.sleep(15)
                                except ConnectionAbortedError as e:
                                    # Not authorized etc.
                                    print(e)
                                except Exception as e:
                                    print(e)
                                    download_successful = False
                            # stopwatch end
                        end_time = time.time()
                        # ToDo: Time_to_result could be improved by measuring the time it takes until the images are
                        #  ready to be downloaded, instead of measuring when they finished downloading
                        time_to_result = end_time - start_time
                        print('Downloading results took ' + str(time_to_result) + ' seconds')
                        if self.offline_mode:
                            download_successful = True

                        self._jobs_names.append(job_identifier)
                        details = {
                            'backend': provider['name'],
                            'job': job_identifier,
                            'file': file_path,
                            'validation-rules-path': path_to_validation_rules,
                            'time_to_result': time_to_result,
                            'download_successful': download_successful
                        }
                        self.results.append(details)

        self._jobs_names = set(self._jobs_names)



import os
import time
import json
import uuid

import openeo
from openeo.auth.auth_bearer import BearerAuth


class JobWorker:
    def __init__(self, backend_providers):
        self.results = []
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
        for provider in self.backendProviders['providers']:
            user = provider['credentials']['user']
            password = provider['credentials']['password']

            con = openeo.connect(provider['baseURL'], auth_type=BearerAuth,
                                 auth_options={"username": user, "password": password})
            cap = con.capabilities()

            print(cap.version())

            job_directory = 'openeo-sentinel-reference-jobs/'
            # In the future, the regions layer could be removed, it is not factual information but just a pattern for myself
            regions = [f.path for f in os.scandir(job_directory) if f.is_dir()]

            for region in regions:
                print(region)
                dirpath = os.path.join(region, provider['name'])
                jobs = [f.path for f in os.scandir(dirpath) if f.is_dir()]
                print(jobs)

                for job in jobs:
                    process_graphs = [f for f in os.listdir(job) if os.path.isfile(os.path.join(job, f))]
                    path_to_process_graph = os.path.join(job, process_graphs[0])
                    print(job)
                    with open(path_to_process_graph, 'r') as process_graph:
                        process_graph = json.loads(process_graph.read())

                        save_path = job.replace(job_directory, 'reports/')

                        if not os.path.exists(save_path):
                            os.makedirs(save_path)

                        file_uuid = str(uuid.uuid4())
                        file_path = save_path + '/' + file_uuid + '.' + 'png'
                        print(file_path)
                        # Todo: Count the time it takes to retrieve the results
                        download_successful = False
                        use_backends = True
                        if use_backends is True:
                            # stopwatch starting
                            if provider['name'] == 'EURAC':
                                con.download(process_graph, 0, file_path, {'format': 'PNG'})
                                download_successful = True
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
                                            print('Retrying to download file in 5 seconds')
                                            print(openEO_job.describe_job())
                                            time.sleep(15)
                                except ConnectionAbortedError as e:
                                    """ Unauthorized """
                                    print(e)
                            # stopwatch end
                        if download_successful or use_backends is False:
                            # ToDo: Fix naming and process
                            job_identifier = region.split('/')[1] + '-' + job.split('/')[-1]
                            self._jobs_names.append(job_identifier)
                            details = {
                                'backend': provider['name'],
                                'job': job_identifier,
                                'file': file_path
                            }
                            self.results.append(details)

        self._jobs_names = set(self._jobs_names)



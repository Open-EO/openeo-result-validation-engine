import os
import time

import openeo
from openeo.auth.auth_bearer import BearerAuth


class JobWorker:
    def __init__(self, backend_providers, reference_job):
        self.results = []
        self.backendProviders = backend_providers
        self.referenceJob = reference_job
        self._jobs = []

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
        if self._jobs:
            return self._jobs.pop()
        else:
            return None

    def get_all_jobs(self):
        jobs = []
        for current_job in self._jobs:
            imagery = []
            for result in self.results:
                if result['job'] == current_job:
                    imagery.append(result)
            jobs.append(imagery)
        return jobs

    def start_fetching(self):
        for provider in self.backendProviders['providers']:
            user = provider['credentials']['user']
            password = provider['credentials']['password']

            con = openeo.connect(provider['baseURL'], auth_type=BearerAuth,
                                 auth_options={"username": user, "password": password})
            cap = con.capabilities()

            print(cap.version())

            if provider['name'] in ['EURAC', 'GEE', 'R', 'Python']:
                for job in provider['jobs']:
                    save_path = "job_results/" + job['name']
                    print(save_path)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    file_path = save_path + '/' + provider['name'] + '_' + job['name'] + '.' + job['output_format']

                    if provider['name'] == 'EURAC':
                        con.download(job['process_graph'], 0, file_path, {"format": job['output_format']})
                    else:
                        openEO_job = con.create_job(job['process_graph'], output_format=job['output_format'])
                        openEO_job.start_job()
                        download_finished = False
                        while download_finished is not True:
                            try:
                                openEO_job.download_results(file_path)
                                download_finished = True
                            except ConnectionAbortedError:
                                download_finished = False
                                print('Retrying to download file in 5 seconds')
                                time.sleep(5)

                    self._jobs.append(job['name'])
                    details = {
                        'backend': provider['name'],
                        'job': job['name'],
                        'file': file_path
                    }
                    self.results.append(details)
                    print(self.results)
        self._jobs = set(self._jobs)



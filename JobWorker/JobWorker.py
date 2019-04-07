import requests
import requests_mock


class JobWorker:
    def __init__(self, backend_providers, reference_job):
        self.results = []
        self.backendProviders = backend_providers
        self.referenceJob = reference_job
        self._jobs = []

    def get_results(self):
        current_job = self.next_job()
        imagery = []
        for result in self.results:
            if result['job'] == current_job:
                imagery.append(result)
        return imagery

    def next_job(self):
        return self._jobs.pop()

    def start_fetching(self):
        # ToDo: In the future, this job worker would use the OpenEO Python client to connect to various
        #  backend Providers and send the process graph of the validation job to all configured backend providers
        for provider in self.backendProviders['providers']:
            session = requests.Session()
            adapter = requests_mock.Adapter()
            session.mount('mock', adapter)
            if provider['name'] in ['EURAC', 'GEE']:
                for job in provider['jobs']:
                    self._jobs.append(job['job'])
                    for file in job['files']:
                        adapter.register_uri('GET', 'mock://test.com/1', json={'backend': provider['name'],
                                                                               'job': job['job'], 'file': file},
                                                                                status_code=200)
                        details = session.get('mock://test.com/1').json()
                        self.results.append(details)
        self._jobs = set(self._jobs)



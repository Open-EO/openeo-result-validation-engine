import requests
import requests_mock


class JobWorker:
    def __init__(self, backend_providers, reference_job):
        self.results = []
        self.backendProviders = backend_providers
        self.referenceJob = reference_job

    def get_results(self):
        return self.results

    def start_fetching(self):
        ## print(self.backendProviders['providers'])
        # ToDo: In the future, this job worker would use the OpenEO Python client to connect to various
        #  backend Providers and send the process graph of the validation job to all configured backend providers
        for provider in self.backendProviders['providers']:
            session = requests.Session()
            adapter = requests_mock.Adapter()
            session.mount('mock', adapter)
            if provider['name'] in ['EURAC', 'GEE']:
                for file in provider['files']:
                    adapter.register_uri('GET', 'mock://test.com/1', json={'backend': provider['name'], 'file': file }, status_code=200)
                    self.results.append(session.get('mock://test.com/1').json())


            for file in files:
                self.results.append(requests.get(
                    'http://localhost:8000/job/id/results').text)

    def run_processgraph(session, pg):
        headers = {'Authorization': 'Bearer e4d96fd79ab8dd37'}
        with session.post("https://earthengine.openeo.org/v0.3/preview", headers=headers, json=pg) as response:
            print('response: {}'.format(response.content))

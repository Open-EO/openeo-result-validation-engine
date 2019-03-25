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
        with requests_mock.Mocker() as m:
            files = [{'text': 'mock/min-time/backend.png', 'status_code': 200},
                     {'text': 'mock/min-time/backend2.png',
                       'status_code': 200},
                     {'text': 'mock/min-time/backend3.png',
                       'status_code': 200},
                     {'text': 'mock/min-time/backend4.png', 'status_code': 200},
                     {'text': 'mock/min-time/backend5-wrong-resolution.png', 'status_code': 200},
                     {'text': 'mock/min-time/backend.jpg',
                      'status_code': 200},
                     {'text': 'mock/min-time/backend-smaller-resolution-exportedwithGimp.png',
                      'status_code': 200},
                     ]

            m.get('http://localhost:8000/job/id/results', files
                  )

            for file in files:
                self.results.append(requests.get(
                    'http://localhost:8000/job/id/results').text)

    def run_processgraph(session, pg):
        headers = {'Authorization': 'Bearer e4d96fd79ab8dd37'}
        with session.post("https://earthengine.openeo.org/v0.3/preview", headers=headers, json=pg) as response:
            print('response: {}'.format(response.content))

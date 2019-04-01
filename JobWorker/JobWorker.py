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
            test_file_selection = 'simple'
            if test_file_selection == 'simple':
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
            elif test_file_selection == 'classification':
                files = [{'text': 'mock/min-time/classification.jpg', 'status_code': 200},
                         {'text': 'mock/min-time/classification_2.jpg', 'status_code': 200}]
            else:
                files = [{'text': 'mock/min-time/RealFilesizes/Backend.jp2', 'status_code': 200},
                         {'text': 'mock/min-time/RealFilesizes/T19NGH_20190120T145729_TCI_10m Kopie 2.jp2', 'status_code': 200}]

            m.get('http://localhost:8000/job/id/results', files
                  )

            for file in files:
                self.results.append(requests.get(
                    'http://localhost:8000/job/id/results').text)

    def run_processgraph(session, pg):
        headers = {'Authorization': 'Bearer e4d96fd79ab8dd37'}
        with session.post("https://earthengine.openeo.org/v0.3/preview", headers=headers, json=pg) as response:
            print('response: {}'.format(response.content))

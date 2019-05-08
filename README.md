# openeo-validation-engine

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/072695f2ebbb404cb0512b711efa76d4)](https://app.codacy.com/app/simonschulte1991/openeo-validation-engine?utm_source=github.com&utm_medium=referral&utm_content=Sijoma/openeo-validation-engine&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.com/Sijoma/openeo-validation-engine.svg?branch=master)](https://travis-ci.com/Sijoma/openeo-validation-engine)

The openeo-validation-engine uses the [OpenEO-sentinel-reference-jobs](https://github.com/Sijoma/openeo-sentinel-reference-jobs) as a submodule and fetches the results of these jobs from every specified back-end provider. The results are then validated and a report is generated for each job. These reports are then pushed to the gh-pages branch of this repository.

Due to filesize limitations, comparison images are currently not stored in this process.


## Installation
We mostly use Python3 in a venv environment. The following commands have to be run sequentially to install the application and its dependencies.

```bash
git clone --recursive https://github.com/Sijoma/openeo-validation-engine
cd openeo-validation-engine
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
cd openeo-python-client
pip install -r requirements.txt
pip install -e .
```

## Configuration

OpenEO back-end providers can be added in the backendProvider.json. This JSON contains an array of JSON objects that 
contain the information for a given provider.

* `name`: The name of the backend-provider.
* `baseURL`: The address of the openEO API endpoint from the backend-provider.
* `credentials`: The account information required to authenticate openEO requests.
    * `user`: The username, this is optional and can be left empty
    * `password`: The password to authenticate, this is optional and can be left empty

```json
      {
      "name": "openEO-GEE",
      "baseURL": "https://earthengine.openeo.org/v0.3",
      "credentials": {
        "user": "Example",
        "password": "Example123"
        }
      }
```

### Reference jobs

Reference jobs (jobs that are validated) can be added in the folder `openeo-sentinel-reference-jobs`. They are currently
separated by arbitrary regions to make it a bit easier to distinguish them. Each Job has a folder that should be called
Job-N (N is the counter). This folder then has to contain a folder that matches the `name` specified in the backendProvider.json,
e.g. `openEO-GEE` in our current example. This folder then contains a single process graph.

Validation rules can be configured on a per job basis, in a file called `validation-rules.json`. There are three possible options:

* Specifying no rules; `default` validation rules get selected (stored in the folder `rule-configurations`)
* Specifying a `name` of a ruleset; the validation engine then tries to find a json file with the name `name`-validation-rules.json
```json
{
  "ruleset-name": "quick"
}
```
* Specifying validation rules directly inside the json.
```json
{
  "validation": {
      "rules": {
          "input-data-checks": {
          },
          "output-data-checks": {
              "matching-file-extensions": "png",
              "file-size-check": true
          },
          "color-checks": {
              "threshold": 1.2
          },
          "pixel-checks": {
            "resolution-allow-divergence": 0.5,
            "image-similarity-measures": 1.0,
            "resize-factor": 0.05
          },
          "classification-checks": {
            "matching-boundaries": "0.20",
            "resize-factor": 0.05
          },
          "nan-value-check": {
              "allow-nan": true,
              "correct": 0
          }
      }
  }
}
```

## Run
Activate the Python venv (`source venv/bin/activate`) and start the ValidationEngine with `python ValidationEngine.py`


### Additional CLI arguments

If you want to prevent the validation engine from downloading the same OpenEO jobs again you can pass the argument --offline True.
`python ValidationEngine.py --offline True`

To speed up the validation, a resize factor can be used. This factor reduces the size of the image and thus all computations are quicker. A value of 0.10 results in an image that is 10% of the original size.

`python ValidationEngine.py --resize 0.10`

## Validation against local files
Add a similar json-object as the one below to the `backendProvider.json`.

```json
  {
    "name": "Local-Python",
    "local": true
  }
```

In the folder `openeo-sentinel-reference-jobs`, add a folder with the `name` of the backend provider, e.g. `Local-Python`.
This folder then should contain a json that stores the path to the locally stored file instead of the process-graph.

```json
{
  "file": "/Users/simon/Documents/Uni/MasterThesis/openeo-sentinel-reference-jobs/Switzerland/Python/RawData/Python_NDVI_S2A_MSIL2A_20180604T103021_N0208_R108_T32TNT_20180604T165443.tiff"
}
```

This allows to validate local results against openEO cloud-processed results and it also enables validation of just local results.



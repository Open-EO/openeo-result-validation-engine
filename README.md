# openeo-result-validation-engine

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6fe179a5dc8e4ac29bdf94f1e9d40fa4)](https://app.codacy.com/app/m-mohr/openeo-result-validation-engine?utm_source=github.com&utm_medium=referral&utm_content=Open-EO/openeo-result-validation-engine&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/Open-EO/openeo-result-validation-engine.svg?branch=master)](https://travis-ci.org/Open-EO/openeo-result-validation-engine)

The openeo-validation-engine uses the [OpenEO-sentinel-reference-jobs](https://github.com/Sijoma/openeo-sentinel-reference-jobs) as a submodule and fetches the results of these jobs from every specified back-end provider. The results are then validated and a report is generated for each job. These reports are then pushed to the gh-pages branch of this repository.

Due to filesize limitations, comparison images are currently not stored in this process.


## Installation
We use Python3 in a venv environment. Using a venv is not necessary but recommended. The following commands have to be run sequentially to install the application and its dependencies.

```bash
git clone --recursive https://github.com/Open-EO/openeo-result-validation-engine
cd openeo-result-validation-engine
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
      "name": "WWU_GEE",
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
              "file-size-check": 0.2
          },
          "color-checks": {
            "threshold-correlation": 0.5,
            "threshold-intersection": 345,
            "threshold-chi-squared": 1500,
            "threshold-hellinger": 0.5,
            "threshold-chi-square-alt": 5000,
            "threshold-kullback-leibler": 5000
          },
          "pixel-checks": {
            "resolution-allow-divergence": 0.5,
            "image-similarity-measures": 0.95,
            "resize-factor": 0.5
          },
          "classification-checks": {
            "matching-boundaries": 0.20,
            "resize-factor": 0.5
          },
          "nan-value-check": {
            "allow-nan": false
          }
      }
  }
}
```

## Usage

Activate the Python venv and start the ValidationEngine.

```bash
source venv/bin/activate
python ValidationEngine.py
```

### Additional CLI arguments

Run `python ValidationEngine.py --help` to get information on all available CLI commands.

If you want to prevent the validation engine from downloading the same OpenEO jobs again you can pass the argument `--offline True`.
Example:
`python ValidationEngine.py --offline True`

To speed up the validation, a resize factor can be used. This factor reduces the size of the image and thus all computations are quicker. A value of 0.10 results in an image that is 10% of the original size. This of course reduces the quality of the validation.

Example:
`python ValidationEngine.py --resize 0.10`

Mocked examples (jobs stored in the folder mock-examples) can be run with:

```bash
python ValidationEngine.py --mock True 
```

To run only a specific reference job, the job-identifier can be passed as an argument.
The structure of the id is as follows: <Region>-Job-<Number>
Examples: Island-Job-2, Netherlands-Job-2

```bash
python ValidationEngine.py --refJob Switzerland-Job-1 
```


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
  "file": "/path/to/file/file.tiff"
}
```

This allows to validate local results against openEO cloud-processed results and it also enables validation of just local results.

## Validation "Studies"

The ValidationEngine runs every 24 hours to compute the validation results for two "studies". 

Validation reports for the comparison between back-end providers EURAC and WWU/GEE can be found in the branch [gh-pages](https://github.com/Open-EO/openeo-result-validation-engine/tree/gh-pages) of this repository. It only contains the JSON reports as the raw data from EURAC is to large.

Validation reports for the comparison between the COPERNICUS/S2 and COPERNICUS/S2_SR data set of the WWU/GEE back end can be found in the branch [reports-GEE_S2-vs-GEE_SR](https://github.com/Open-EO/openeo-result-validation-engine/tree/reports-GEE_S2-vs-GEE_SR) of this repository. These branch also contains imagery, as we are not able to retrieve native resolution from the WWU/GEE back end and thus are able to store the images on GitHub.

## Encrypting Git Token

To publish the validation reports to Github this repository needs a valid GitHub Token.

1. install the Travis CI Command Line Client by running 
`gem install travis` and login with `travis login --org`
2. Generate SSH-KEY
`ssh-keygen -t rsa -b 4096 -C "your_github_email@example.com"`
3. Add deploy_key.pub to the repository https://github.com/Open-EO/openeo-result-validation-engine/settings/keys
4. Encrypt the deploy_key.pub file with the Travis CLI `travis encrypt-file deploy_key --add (This will generate an encryption label)`
5. Adjust encryption label in .travis.yml line 21

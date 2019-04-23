# openeo-validation-engine

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/072695f2ebbb404cb0512b711efa76d4)](https://app.codacy.com/app/simonschulte1991/openeo-validation-engine?utm_source=github.com&utm_medium=referral&utm_content=Sijoma/openeo-validation-engine&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.com/Sijoma/openeo-validation-engine.svg?branch=master)](https://travis-ci.com/Sijoma/openeo-validation-engine)

The openeo-validation-engine uses the [OpenEO-sentinel-reference-jobs](https://github.com/Sijoma/openeo-sentinel-reference-jobs) as a submodule and fetches the results of these jobs from every specified back-end provider. The results are then validated and a report is generated for each job. These reports are then pushed to the gh-pages branch of this repository.

Due to filesize limitations, comparison images are currently not stored in this process.

## Prerequisites

### Platform Prerequisites

Have access to a Red Hat OpenShift platform (tested on 4.7.x and 4.8.x).
Install the following operators from Operator hub. Please be patient and wait for each operator to be installed before proceeding to the next one:
* Red Hat Integration AMQ Streams (v. 1.8.2)
* OpenShift Container Storage (v. 4.8.3)
* Red Hat OpenShift Serverless (v. 1.18.0)
* Open Data Hub Operator (v. 1.1.1)
* Red Hat OpenShift Pipelines (v. 1.5.2) - optional, may be used to create automated build/deploy pipelines triggered by Git change web-hooks.

***Note!*** The scenario assumes the use of AWS S3-compatible buckets provided by OpenShift Container Storage. If you want to use regular AWS S3 buckets or other type of storage, please adjust the code of the applications/utilities that require access to storage.



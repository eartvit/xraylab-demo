# X-Ray Lab
Showcase of an intelligent application for pneumonia risk detection using Machine Learning model workloads on Red Hat OpenShift.

## Foreword
This demo is a variant of the one created by Guillaume Moutier which can be found in this repo [Red Hat Data Services - Jumpstart library - XRay Pipeline](https://github.com/red-hat-data-services/jumpstart-library/tree/main/demo1-xray-pipeline), however the focus here is on the developer and data scientist experience for developing and deploying ML models and intelligent applications on Red Hat OpenShift. While several items have been reused (to some extent) from the before mentioned repository, this repository also contains a front end webapp to visualize the results.

The main idea behind this showcase is to demonstrate the end to end capabilities of Red Hat Openshift for developing and deploying integrated Machine Learning workloads.

Please note the solution has been tested on Red Hat OpenShift 4.7.x and 4.8.x and may require some changes on other versions of the platform.

## Let's get started
Recent advances in the field of Machine Learning have made very attractive its use to researchers and developers. One of such advancement is in the image processing and analysis domain and this showcase presents an intelligent application ecosystem that uses Convolutional Neural Networks (CNN) to process labeled x-ray images for pneumonia risk detection purposes to help health practitioners in their daily work (i.e., performing patient triage based on the prediction of the ML model).

### Prerequisites
Please ensure you have the setup as described in the [prerequisites](https://github.com/eartvit/xraylab-demo/tree/main/prerequisites) folder before continuing to the next section.

### Showcase overview
The scenario focuses on the following user stories:
* As a data scientist, I want to develop an image classification model for chest x-ray images using Jupyter Hub (lab/notebooks) as my preferred research environment.
* As a data scientist, I want my model to be deployed quickly so that it may be used by other applications.
* As a (fullstack) developer, I want to have quick access to resources that support the business logic of my applications, including databases, storage, messaging.
* As a (fullstack) developer, I want an automated build process to support new releases/code updates as soon as they are available in a git repository.
* As an operations engineer, I want an integrated monitoring dashboard to new applications available on the (production) infrastructure.

### The Data Scientist user stories details



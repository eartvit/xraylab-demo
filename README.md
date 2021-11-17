# X-Ray Lab
Showcase of an intelligent application for pneumonia risk detection using Machine Learning model workloads on Red Hat OpenShift.

## Foreword
This showcase is a variant of the one created by Guillaume Moutier which can be found in this repo [Red Hat Data Services - Jumpstart library - XRay Pipeline](https://github.com/red-hat-data-services/jumpstart-library/tree/main/demo1-xray-pipeline), however the focus here is on the developer and data scientist experience for developing and deploying ML models and intelligent applications on Red Hat OpenShift. While several items have been reused (to some extent) from the before mentioned repository, this repository also contains a front end webapp to visualize the results.

The main idea behind this showcase is to demonstrate the end to end capabilities of Red Hat Openshift for developing and deploying integrated Machine Learning workloads.

Please note the solution has been tested on Red Hat OpenShift 4.7.x and 4.8.x and may require some changes on other versions of the platform.

## Let's get started
Recent advances in the field of Machine Learning have made very attractive its use to researchers and developers. One of such advancement is in the image processing and analysis domain and this showcase presents an intelligent application ecosystem that uses Convolutional Neural Networks (CNN) to process labeled x-ray images for pneumonia risk detection purposes to help health practitioners in their daily work (i.e., performing patient triage based on the prediction of the ML model).

### Prerequisites
Please ensure you have the setup as described in the [prerequisites](https://github.com/eartvit/xraylab-demo/tree/main/prerequisites) folder before continuing to the next section.

### Showcase overview
The main idea built by this showcase is an ecosystem consisting of one or several hospitals and a research centre. At the hospitals, technicians take x-ray images and store them with patient and make them ready for interpretation and analysis to the specialist doctors. This process may be automated and improved by using an inteligent application that analyses x-ray images and makes a prediction that may be then used by doctors to perform triage/prioritization of patiens and to increase their throughput. Building such a system may be done using a supervised machine learning approach where existing labeled images may be used for training of a machine learning model that can distinguish between normal or abnormal images (in our case the abnormal is the pneumonia). Patient privacy is maintained by the means of an anonymization process (in our showcase we skip this since for training purposes we used an anonymized Kaggle dataset with labeled [pneumonia](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia) images. These images are then used to train an ML model that recognizes pneumonia use cases. This model is deployed as service (may be centralized and shared with several hospitals). Different hospitals store their x-ray images on a form of storage (OpenShift Container Storage with Rados GW in our case). Using this type of storage (compatible with AWS S3 Bucket API) a notification service may be created to send a message to a Kafka topic, hosted on OpenShift by using the AMQ Streams (which is RedHat's version of Apache Kafka). As part of the notification message it shall be passed the name of the image, the S3 endpoint (since different hospitals may use different endpoints) and the name of the bucket (among other things). On the centralized location where the pneumonia risk detection machine learning model resides, a [listener application](https://github.com/eartvit/xraylab-demo/tree/main/pneumonia-kafka-lstnr) can be triggered a knative-kafka event from OpenShift to extract the payload to be passed to the pneumonia risk service. The [risk detection service](https://github.com/eartvit/xraylab-demo/tree/main/pneumonia-risk-detection) retrieves the image using the provided information, analyzes it and performs the prediction which is stored in a database (i.e., MySQL) then deletes the image. (Naturally, if the hospital ecosystem and the risk detection application are completely separate then passing back the results should be done by using other micro-services or another Kafka topic - in this showcase this aspect is simplified and skipping ahead to the point where the results are stored in some database). Lastly, a doctor may review the results by the means of a [web app](https://github.com/eartvit/xraylab-demo/tree/main/utils/xrayweb) that exposes patien information, x-ray images, and prediction results (in this showcase the webapp offers minimal functionality just to complete the end-to-end scenario).
The entire concept is depicted in the below diagram:
![showcase](docs/showcase.png)

Random images from the before mentioned Kaggle dataset have then been modified to contain fictional patient information. These images are simulating the x-ray technician's work at a hospital that are uploaded to a source bucket that is being monitored by a listener service that sends notifications to Kafka. In our showcase, this is simulated by the [image-uploader](https://github.com/eartvit/xraylab-demo/tree/main/utils/image-uploader) application.


The purpose of the showcase is to describe the steps required to build the ecosystem implementing the pneumonia risk detection ecosystem and it focuses on the following user stories:
* As a data scientist, I want to develop an image classification model for chest x-ray images using Jupyter Hub (lab/notebooks) as my preferred research environment.
* As a data scientist, I want my model to be deployed quickly so that it may be used by other applications.
* As a (fullstack) developer, I want to have quick access to resources that support the business logic of my applications, including databases, storage, messaging.
* As a (fullstack) developer, I want an automated build process to support new releases/code updates as soon as they are available in a git repository.
* As an operations engineer, I want an integrated monitoring dashboard to new applications available on the (production) infrastructure.

### The Data Scientist user stories details
Data scientists typically use Jupyter Notebooks in order to perform their work. OpenShift's Open Data Hub project makes available several different Jupyter images for this purpose. 
To get started, head to your OpenShift web console and select the project where the Open Data Hub instance has been deployed (see the [prerequisites](https://github.com/eartvit/xraylab-demo/tree/main/prerequisites)). Then go to Networking->Routes and click on the ODH dashboard. From there you have access to Jupyter Hub/Lab (depending on the version of OpenShift and ODH you used either hub or lab are available). 
![odh-routes](docs/odh-routes.png)
![odh-dashboard](docs/odh-dashboard.png)
The first time you instantiate Jupyter it will ask to accept/allow some permissions to be set: 
![jupyther-authorize](docs/jupyter-authorize-1.png)
Then you can create a notebook server (select medium size for this showcase).
![jupyter-medium-ds-image](docs/jupyter-medium-ds-image-1.png)
Now the environment is prepared to kick-off the work of the data scientists. This showcase stores a sample model training notebook and some additional notebooks required to setup the S3 buckets and the SNS notification service to trigger kafka messages whenever a new image is uploaded to an input bucket. To obtain these notebooks from the current repository, create a new notebook in the Jupyter instance and enter the following commands in a code cell and execute them:
```
!pip install git+git://github.com/HR/github-clone
!pip install tensorflow
!pip install boto3
!ghclone https://github.com/eartvit/xraylab-demo/tree/main/notebooks
```
You should see after the completion of the commands that a new directory `notebooks` has been created within your jupyter hub instance:
![odh-notebooks](docs/odh-notebooks.png)

Inside the notebooks folder there are three Jupyter notebooks:
* One example of [pneumonia risk detection ML model](https://github.com/eartvit/xraylab-demo/blob/main/notebooks/x-ray-predict-pneumonia-tf-training.ipynb) creation notebook. Here you can see the steps how the sample model was created.
* One [S3 buckets creation](https://github.com/eartvit/xraylab-demo/blob/main/notebooks/s3-buckets.ipynb) notebook. Please use this notebook to create the necessary buckets for simulation of the "production" scenario where the deployed ML model is integrated with the other applications described in the `Showcase overview` section of this readme document (you can run this notebook at this time).
* One [SNS notification](https://github.com/eartvit/xraylab-demo/blob/main/notebooks/create_notifications.ipynb) notebook used to setup the SNS service that shall trigger a new Kafka message every time an x-ray image is uploaded in the source bucket (also used in the "production" scenario). Please do not run this notebook yet as it should be run after the Kafka instance has been created (in the next section).

***Note!*** In case you wish to change and retrain the ML model then first you will need to upload the train-test-validation set to the train-test-validation bucket (see [S3 buckets creation](https://github.com/eartvit/xraylab-demo/blob/main/notebooks/s3-buckets.ipynb) for details on how to create the bucket). To upload the images you can do that easily by using the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) as follows:
```shellscript
aws s3 sync --profile=<xraylab_profile_name> --endpoint=<external Rados GW endpoint>  . s3://<train-test-validation-bucket>/
```
Please note the above command assumes you created a AWS CLI profile using the AWS KEY_ID and SECRET_KEY of the Rados user as explained in the [prerequisites](https://github.com/eartvit/xraylab-demo/tree/main/prerequisites) and you created the train-test-validation bucket as described in the [S3 buckets creation](https://github.com/eartvit/xraylab-demo/blob/main/notebooks/s3-buckets.ipynb) notebook.

Coming back to our datascientist user stories, naturally, as soon as the datascientist has an ML model ready, it wants it deployed to production fast and easy. One way to do this is by using [Seldon](https://www.seldon.io/).
Seldon core comes a packaged web-server exposing endpoints for accessing the prediction function of a model as well as metrics (including custom ones) for the ML model. Seldon also has pre-packaged inference servers meaning that one can deploy a trained model (i.e. from a pickle or h5 file) just by creating a seldon deployment specification yaml file and without writing any additional code. In our use case since we deal with images taking this approach would make the calling service extremely complicated since it would require to receive as input a tensor object (which is a three dimensional matrix). Luckily with Seldon we can create a simple object following a defined pattern recognized by seldon-core in order to expose our model in a simple way. The [TestXray.py](https://github.com/eartvit/xraylab-demo/blob/main/pneumonia-risk-detection/TestXRay.py) in the [pneumonia-risk-detection](https://github.com/eartvit/xraylab-demo/tree/main/pneumonia-risk-detection) folder is in our showcase the implementation of such an extension. In its most basic form, the class exposing the ML model must contain the initializer (`__init__` function), the `predict` function which Seldon binds it to the `/predict` endpoint of the web-service, and the `metrics` function which is bound to the `/metrics` endpoint queried by Prometheus. The metada initializer is an optional function though it's good practice to create it to have an idea what the `/predict` expects as input array. The additional function used in the code is to accomodate the business logic described in the overview section.

Note that the [TestXray.py](https://github.com/eartvit/xraylab-demo/blob/main/pneumonia-risk-detection/TestXRay.py) does not contain any web server specific code since that is handled behind the scenes directly by Seldon. Therefore the datascientist can focus only on what the model requires as input in order to create a prediction.

Now that we have a model trained and a template service created it's time to deploy them. OpenShift has a way of creating container images directly from source code called Source-to-Image (S2I). We shall use this functionality in our showcase to deploy all the applications of the showcase in the next section, the (fullstack) application developer user stories. 

### The (Fullstack) Application Developer user stories details

A developer wants to have quick access to resources including supporting applications required to be integrated with a custom developed application so that the developer can focus most if the time on writing code that fulfills the business logic of a system. OpenShift offers fast provisioning of certain resources for development purposes of databases (using templates) as well as of Kafka instances. 

Another important aspect to keep track of is having configurations to different entities external to an application, and have them shared accross multiple applications. Openshift uses Secrets and ConfigMaps to store secret keys and configuration values shared among applications.
In our showcase we reuse among different applications the following resources:
* the AWS keys from the Rados GW setup (created in the [prerequisites](https://github.com/eartvit/xraylab-demo/tree/main/prerequisites) section).
* the Rados GW endpoint route to make accessible the images
* the database where the pneumonia-risk-service will write predictions and from where the xray webapp shall read results.

Let's create them by selecting the xraylab project as active in Administrator view and then navigate to Workloads->Secrets. Using the Create command (on the right side) select the key/value secret option
![create-secret](docs/create-secrets-1.png) 
Below is provided a view for the database secrets. Please create another secret for the AWS keys (using the values you obtained in the prerequisites section)
![create-secret-db](docs/create-secrets-2.png)

Next, let's create a configuration map for the S3 buckets endopoint URL followin a similar approach but this time selecting Workloads->ConfigMaps. Note that in the case of ConfigMaps you will need to work with yaml content. Eventually your file should look similar to the one below:
![config-maps](docs/config-maps-1.png)

Next, as per our showcase description we need a few other resources before we can continue to application deployment:
* a Kafka instance with a topic where to write the information about the messages dropped in the S3 bucket
* a database where to store the results
* a Kafka source which shall act as a kafka topic listener and consume messages by directing them to an application - this resource we shall create it after we deploy the listener application.

With Red Hat Openshift provisioning a database is fast and easy. Just switch over to developer view and click add and by default the topology view appears with all the deployed applications and services in a selected user namespace. Ensure the selected project is `xraylab` and then click on "Add" from the left menu:
![developer-add-1](docs/developer-add-1.png)
The available DB templates shall appear. For our showcase we shall use MariaDB. Select the template and click on the instantiate button:
![developer-add-db-1](docs/developer-add-db-1.png)
Update the service name, connection user name, password, root password and database name to the values you created in the db-secret Secret file.
![developer-add-db-2](docs/developer-add-db-2.png)

Wait for the application to be deployed.

Next, we can create our Kafka instance.
...


Let us turn now attention towards the application deployments and let's start with our ML model deployment.
In the Developer view of OpenShift, select the project where you want the application to be deployed (let's assume everything goes to the `xraylab` namespace). Then select add new application and then under the Git Repository section select the `From Dockerfile` tile (given that in our case we have a dockerfile definition for each of the application we are going to deploy).
![developer-add-1](docs/developer-add-1.png)
***Note!*** Source-to-Image (S2I) works also without a Dockerfile, directly with source code and there are several base containers supporting various languages/frameworks. In this showcase the Dockerfile one is presented as it is a very straightforward one considering the applications we want to deploy.

In the next screen fill in the Git repository information (also click on the Show Advanced Git Options link and set the context dir to `/pneumonia-risk-detection` since there it is the Dockerfile which will provide instructions to the S2I builder on how to package the application.
![pneumonia-risk-detection-dpl-1](docs/pneumonia-risk-detection-dpl-1.png)
Next, scroll down to to the resources and select Deployment-Config. This will allow you to directly control the application environment and automatically trigger a new build whenever something is changed. Optionally, you can use pipelines if you installed them.
Next, we need to define the route information and the deployment variables. The dockerfile specifies the default 8080 port already so no need to change that. It is however advised to use secure routes. Therefore click on Secure Route checkbox and for TLS termination select "Edge" and "Redirect" for the Insecure Traffic options.
![pneumonia-risk-detection-dpl-2](docs/pneumonia-risk-detection-dpl-2.png)
Next, scroll down to the bottom of the page and click on deployment:
![pneumonia-risk-detection-dpl-3](docs/pneumonia-risk-detection-dpl-3.png)
Here we can define the environment variable used by the application:



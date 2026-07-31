# Transport Booking Agent (VS Code Guide)

This guide provides instructions for developing and deploying the Transport Booking Agent application using the Cloud Code extension for Visual Studio Code. The Transport Booking Agent is an AI-powered multi-agent system for booking transport, with its full technical specification detailed in `docs/SPEC.md`. When you run the application, Cloud Code uses [skaffold](https://skaffold.dev/docs/) under the hood to build an image and deploy the project's Kubernetes manifests. To learn more about Kubernetes, explore the [Kubernetes overview](https://kubernetes.io/docs/concepts/overview/).
### Table of Contents
* [What's in this sample](#whats-in-this-sample)
* [Getting Started](#getting-started)
    1. [Set up a Kubernetes cluster](#set-up-a-kubernetes-cluster)
        * [Minikube](#minikube) - free local cluster
        * [GKE](#GKE) - Google Kubernetes Engine
    2. [Deploy app to cluster](#deploy-app-to-cluster)

---
## What's in this sample
### Kubernetes architecture
![Kubernetes Architecture Diagram](../../img/diagram.png)

<h3 id="directory-contents"> Directory contents </h3>

- `kubernetes-manifests/` - Contains Kubernetes YAML files for the Transport Booking Agent services and deployments, including:

  - `transport-booking-agent.deployment.yaml` - deploys a pod with the 'transport-booking-agent' container image
  - `transport-booking-agent.service.yaml` - creates a load balancer and exposes the 'transport-booking-agent' service on an external IP in the cluster


---
## Getting Started

### Set up a Kubernetes cluster

#### Minikube
 
 Cloud Code uses [minikube](https://minikube.sigs.k8s.io/docs/) to create a free local cluster.

1. Navigate to the **Clusters** explorer in the Cloud Code - Kubernetes sidebar using the left side Activity bar.

> Note: in newer versions of VS Code, the **Clusters** explorer has been replaced with a dedicated **Kubernetes** section.

2. Click '+' in the title bar of the Clusters explorer to create a new cluster. If prompted, follow the instructions to log in to Google Cloud Platform.  

3. Choose **Minikube** and then select **minikube**. 

2. Select **Start**. Cloud Code will initiate a minikube cluster.

#### Google Kubernetes Engine

1. Navigate to the **Clusters** explorer in the Cloud Code - Kubernetes sidebar using the left side Activity bar.

> Note: in newer versions of VS Code, the **Clusters** explorer has been replaced with a dedicated **Kubernetes** section.

2. Click '+' in the title bar of the Clusters explorer to create a new cluster. If prompted, follow the instructions to log in to Google Cloud Platform.  

3. Choose **Google Kubernetes Engine**. If you have existing clusters associated with your GCP project, you can select one from this dialog. To create a new cluster, click **+ Create a new GKE Cluster** and follow these steps:

    a. Choose **Standard** or **Autopilot**. For more information, see [Comparing Autopilot and Standard modes](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview#comparison?utm_source=ext&utm_medium=partner&utm_campaign=CDR_kri_gcp_cloudcodereadmes_012521&utm_content=-).

    b. If prompted, click **Open** to permit Cloud Code to open the Cloud Console.

    c. In the Cloud Console, choose any configuration options that you want to customize and then click **Create**.

    d. Once the cluster has finished being created, return to VS Code and click **Refresh**.

    You can now select your newly created cluster.

8. The cluster you select will be added to the **Clusters** explorer and set as the default context. You can inspect the cluster's properties, make changes to the cluster's resources, and view logs by clicking the dropdown arrow next to the cluster name in the **Clusters** explorer.

### Deploy app to cluster

1. Navigate to the **Development Sessions** explorer in the **Cloud Code - Kubernetes** sidebar using the Activity bar on the left side of the IDE.

2. Click the 'Play' icon in the title bar of the **Development Sessions** explorer to run the application. If prompted, confirm the current context and image registry.

3. View the build progress in the **Development Sessions** explorer. Once the build has finished, the URLs for your deployed app will be displayed under **Port Forward URLs**. Click on the 'Open Window' icon next to the service's URL to visit your deployed app.

4.  To stop the application, click the stop icon on the Debug Toolbar.

If you created a GKE cluster for this tutorial, be sure to delete your cluster to avoid incurring charges.


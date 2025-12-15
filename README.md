CKAN Helm Chart
==========

[![License][]][1][![Chat on Gitter][]][2]

<!-- Badge references -->
[License]: https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=flat
[1]: https://opensource.org/licenses/Apache-2.0
[Chat on Gitter]: https://badges.gitter.im/gitter.svg
[2]: https://gitter.im/keitaroinc/docker-ckan

A Helm chart for CKAN

Current chart version is `4.0.5`

This chart deploys a self contained CKAN instance with all of its dependencies. These can be enabled/disabled if they already exist in your infrastructure.

Two jobs for initializing Postgres and SOLR can also be enabled through the values. These will use the provided CKAN environment to set the access permissions for the ckan and datastore DB users as well as create a SOLR collection for the CKAN instance.

## Prerequisites Details
* Kubernetes
* Install [Helm](https://github.com/helm/helm/releases)
* Setup correctly kubectl and kubeconfig setup before running helm.

## Helm repo
The CKAN and dependency charts can be found on Keitaro's helm repo:
```console
$ helm repo add keitaro-charts https://keitaro-charts.storage.googleapis.com
```

## Deploy CKAN on kubernetes cluster
To deploy CKAN on kubernetes cluster with the release name `<release-name>`:
```console
$ helm repo add keitaro-charts https://keitaro-charts.storage.googleapis.com
$ helm install <release-name> keitaro-charts/ckan
```

## Configuration
Production deployment values can be set in values.yaml [here](https://github.com/keitaroinc/ckan-helm/blob/master/values.yaml).
This file contains variables that will be passed to the templates. All configurable values should be placed in this file.
Alternatively, you can specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

## Cleanup
To remove the spawned pods you can run a simple `helm delete <release-name>`.
Helm will however preserve created persistent volume claims, to also remove them execute the commands below.
```console
$ release=<release-name>
$ helm delete $release
$ kubectl delete pvc -l release=$release
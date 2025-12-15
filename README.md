# CKAN Helm Chart

[![License][]][1] [![Chat on Gitter][]][2]

[License]: https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=flat
[1]: https://opensource.org/licenses/Apache-2.0
[Chat on Gitter]: https://badges.gitter.im/gitterHQ/gitter.svg
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
$ helm repo add keitaro-charts [https://keitaro-charts.storage.googleapis.com](https://keitaro-charts.storage.googleapis.com)
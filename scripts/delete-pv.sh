#!/usr/bin/env bash

kubectl delete pvc ckan data-ckan-deployment-zookeeper-0 data-postgres-0 solr-pvc-solr-0

kubectl delete pv pv-0
kubectl delete pv pv-1
kubectl delete pv pv-2
kubectl delete pv pv-3

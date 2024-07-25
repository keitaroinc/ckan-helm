CKAN Helm Chart
==========

[![License][]][1][![Chat on Gitter][]][2]

A Helm chart for CKAN

Current chart version is `1.0.2`

This chart deploys a self contained CKAN instance with all of its dependencies. These can be enabled/disabled if they already exist in your infrastructure.

Two jobs for initializing Postgres and SOLR can also be enabled through the values. These will use the provided CKAN environment to set the access permissions for the ckan and datastore DB users as well as create a SOLR collection for the CKAN instance.

## Prerequisites Details
* Kubernetes 1.9
* Install [Helm](https://github.com/helm/helm/releases)
* Setup correctly kubectl and kubeconfig setup before running helm.

## Helm repo
The datapusher and ckan charts can be found on Keitaro's helm repo:
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
```


## Chart Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://keitaro-charts.storage.googleapis.com | postgresql | 14.0.1 |
| https://keitaro-charts.storage.googleapis.com | redis | 18.12.1 |
| https://keitaro-charts.storage.googleapis.com | solr | 8.7.1 |
| https://keitaro-charts.storage.googleapis.com | datapusher | 1.0.0 |

## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| CkanDBName | string | `"ckan_default"` | Variable for name of the database used by CKAN |
| CkanDBPass | string | `"pass"` | Variable for password for the CKAN database owner |
| CkanDBUser | string | `"ckan_default"` | Variable for username for the owner of the CKAN database |
| DBDeploymentName | string | `"postgres"` | Variable for name override for postgres deployment |
| DBHost | string | `"postgres"` | Variable for name of headless svc from postgres deployment |
| DatapusherName | string | `"datapusher"` | Variable for name override for datapusher deployment |
| DatastoreDBName | string | `"datastore_default"` | Variable for name of the database used by Datastore |
| DatastoreRODBPass | string | `"pass"` | Variable for password for the datastore database user with read access |
| DatastoreRODBUser | string | `"datastorero"` | Variable for username for the user with read access to the datastore database |
| DatastoreRWDBPass | string | `"pass"` | Variable for password for the datastore database user with write access |
| DatastoreRWDBUser | string | `"datastorerw"` | Variable for username for the user with write access to the datastore database |
| MasterDBName | string | `"postgres"` | Variable for name of the master user database in PostgreSQL |
| MasterDBPass | string | `"pass"` | Variable for password for the master user in PostgreSQL |
| MasterDBUser | string | `"postgres"` | Variable for master user name for PostgreSQL |
| RedisName | string | `"redis"` | Variable for name override for redis deployment |
| SolrName | string | `"solr"` | Variable for name override for solr deployment |
| affinity | object | `{}` |  |
| ckan.activityStreamsEmailNotifications | string | `"true"` |  |
| ckan.ckanPlugins | string | `"envvars image_view text_view recline_view datastore datapusher"` | List of plugins to be used by the instance |
| ckan.datapusherCallbackUrlBase | string | `"http://ckan"` | Location of the CKAN k8s service to be used by the Datapusher, overriding the default site url route. |
| ckan.datapusherUrl | string | `"http://datapusher-headless:8000"` | Location of the datapusher service to be used by the CKAN instance |
| ckan.datastore.RoDbName | string | `"datastore_default"` | Name of the database to be used for Datastore |
| ckan.datastore.RoDbPassword | string | `"pass"` | Password for the datastore read permissions user |
| ckan.datastore.RoDbUrl | string | `"postgres"` | Url of the PostgreSQL server where the datastore database is hosted |
| ckan.datastore.RoDbUser | string | `"datastorero"` | Username for the datastore database with read permissions |
| ckan.datastore.RwDbName | string | `"datastore_default"` | Name of the database to be used for Datastore |
| ckan.datastore.RwDbPassword | string | `"pass"` | Password for the datastore write permissions user |
| ckan.datastore.RwDbUrl | string | `"postgres"` | Url of the PostgreSQL server where the datastore database is hosted |
| ckan.datastore.RwDbUser | string | `"datastorerw"` | Username for the datastore database with write permissions |
| ckan.db.ckanDbName | string | `"ckan_default"` | Name of the database to be used by CKAN |
| ckan.db.ckanDbPassword | string | `"pass"` | Password of the user for the database to be used by CKAN |
| ckan.db.ckanDbUrl | string | `"postgres"` | Url of the PostgreSQL server where the CKAN database is hosted |
| ckan.db.ckanDbUser | string | `"ckan_default"` | Username of the database to be used by CKAN |
| ckan.debug | string | `"false"` |  |
| ckan.extraEnv | list | `[]` | An array to add extra environment variables For example: extraEnv:   - name: FOO     value: "bar" |
| ckan.issues.sendEmailNotifications | string | `"true"` |  |
| ckan.liveness.failureThreshold | int | `6` | Failure threshold for the liveness probe |
| ckan.liveness.initialDelaySeconds | int | `10` | Initial delay for the liveness probe |
| ckan.liveness.periodSeconds | int | `10` | Check interval for the liveness probe |
| ckan.liveness.timeoutSeconds | int | `10` | Timeout interval for the liveness probe |
| ckan.locale.default | string | `"en"` |  |
| ckan.locale.offered | string | `"en"` |  |
| ckan.maintenanceMode | string | `"false"` | Set to true to disable CKAN from starting and serve a maintenance page |
| ckan.psql.initialize | bool | `true` | Flag whether to initialize the PostgreSQL instance with the provided users and databases |
| ckan.psql.masterDatabase | string | `"postgres"` | PostgreSQL database for the master user |
| ckan.psql.masterPassword | string | `"pass"` | PostgreSQL master user password |
| ckan.psql.masterUser | string | `"postgres"` | PostgreSQL master username |
| ckan.readiness.failureThreshold | int | `6` | Failure threshold for the readiness probe |
| ckan.readiness.initialDelaySeconds | int | `10` | Inital delay seconds for the readiness probe |
| ckan.readiness.periodSeconds | int | `10` |  |
| ckan.readiness.timeoutSeconds | int | `10` | Timeout interval for the readiness probe |
| ckan.redis | string | `"redis://redis-headless:6379/0"` | Location of the Redis service to be used by the CKAN instance |
| ckan.siteId | string | `"site-id-here"` | Site id |
| ckan.siteTitle | string | `"Site Title here"` | Site title for the instance |
| ckan.siteUrl | string | `"http://localhost:5000"` | Url for the CKAN instance |
| ckan.smtp.mailFrom | string | `"postmaster@domain.com"` |  |
| ckan.smtp.password | string | `"smtpPassword"` |  |
| ckan.smtp.server | string | `"smtpServerURLorIP:port"` |  |
| ckan.smtp.starttls | string | `"true"` |  |
| ckan.smtp.tls | string | `"enabled"` |  |
| ckan.smtp.user | string | `"smtpUser"` |  |
| ckan.solr | string | `"http://solr-headless:8983/solr/ckancollection"` | Location of SOLR collection used by the instance |
| ckan.spatialBackend | string | `"solr"` |  |
| ckan.storagePath | string | `"/var/lib/ckan/default"` | Storage path to be used by the instance |
| ckan.sysadminApiToken | string | `"replace_this_with_generated_api_token_for_sysadmin"` | CKAN system admin API token Needs to be generated via the CKAN UI and replaced after initial deployment |
| ckan.sysadminEmail | string | `"admin@domain.com"` | CKAN system admin email |
| ckan.sysadminName | string | `"ckan_admin"` | CKAN system admin username |
| ckan.sysadminPassword | string | `"PasswordHere"` | CKAN system admin password |
| datapusher.datapusher.chunkSize | string | `"10240000"` | Size of chunks of the data that is being downloaded in bytes |
| datapusher.datapusher.datapusherRewriteResources | string | `"True"` | Enable or disable (boolean) whether datapusher should rewrite resources uploaded to CKAN's filestore, since datapusher takes the CKAN Site URL value for generating the resource URL. Default: False |
| datapusher.datapusher.datapusherRewriteUrl | string | `"http://ckan"` | Sets the rewrite URL that datapushed will rewrite resources that are uploaded to CKAN's filestore. Default: http://ckan:5000 |
| datapusher.datapusher.datapusherSslVerify | string | `"False"` | Enable or disable (boolean) verification of SSL when trying to get resources. Default: True |
| datapusher.datapusher.downloadTimeout | string | `"300"` | Timeout limit of the download request |
| datapusher.datapusher.insertRows | string | `"50000"` | Number of rows to take from the data and upload them as chunks to datastore |
| datapusher.datapusher.maxContentLength | string | `"102400000"` |  |
| datapusher.enabled | bool | `true` | Flag to control whether to deploy the datapusher |
| datapusher.fullnameOverride | string | `"datapusher"` | Name override for the datapusher deployment |
| fullnameOverride | string | `"ckan"` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"keitaro/ckan"` |  |
| image.tag | string | `"2.9.2"` |  |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0].host | string | `"chart-example.local"` |  |
| ingress.hosts[0].paths | list | `[]` |  |
| ingress.tls | list | `[]` |  |
| ingressRoute.enabled | bool | `false` |  |
| ingressRoute.host | string | `"chart-example.local"` | Used in conjunction with a Traefik v2 deployment |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| postgresql.enabled | bool | `true` | Flag to control whether to deploy PostgreSQL |
| postgresql.existingSecret | string | `"postgrescredentials"` | Name of existing secret that holds passwords for PostgreSQL |
| postgresql.fullnameOverride | string | `"postgres"` | Name override for the PostgreSQL deployment |
| postgresql.persistence.size | string | `"1Gi"` | Size of the PostgreSQL pvc |
| postgresql.pgPass | string | `"pass"` | Password for the master PostgreSQL user. Feeds into the `postgrescredentials` secret that is provided to the PostgreSQL chart |
| pvc.enabled | bool | `true` |  |
| pvc.size | string | `"1Gi"` |  |
| pvc.storageClassName | string | `""` |  |
| redis.cluster.enabled | bool | `false` | Cluster mode for Redis |
| redis.enabled | bool | `true` | Flag to control whether to deploy Redis |
| redis.fullnameOverride | string | `"redis"` | Name override for the redis deployment |
| redis.master.persistence.enabled | bool | `false` | Enable redis volume claim |
| redis.master.persistence.size | string | `"1Gi"` | Size of the volume claim |
| redis.usePassword | bool | `false` | Use password for accessing redis |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `80` |  |
| service.type | string | `"ClusterIP"` | Type of the service created for the CKAN pod |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `false` | Specifies whether a service account should be created |
| serviceAccount.name | string | `nil` | The name of the service account to use. If not set and create is true, a name is generated using the fullname template |
| solr.enabled | bool | `true` | Flag to control whether to deploy SOLR |
| solr.fullnameOverride | string | `"solr"` | Name override for the SOLR deployment |
| solr.image.repository | string | `"solr"` | Repository for the SOLR image |
| solr.image.tag | string | `"6.6.6"` | Tag for the SOLR image |
| solr.initialize.configsetName | string | `"ckanConfigSet"` | Name of the config set used for initializing |
| solr.initialize.enabled | bool | `true` | Flag whether to initialize the SOLR instance with the provided collection name |
| solr.initialize.maxShardsPerNode | int | `10` | Maximum shards per node |
| solr.initialize.numShards | int | `2` | Number of shards for the SOLR collection |
| solr.initialize.replicationFactor | int | `1` | Number of replicas for each SOLR shard |
| solr.replicaCount | int | `1` | Number of SOLR instances in the cluster |
| solr.volumeClaimTemplates.storageSize | string | `"5Gi"` | Size of Solr PVC |
| solr.zookeeper.persistence.size | string | `"1Gi"` | Size of ZK PVC |
| solr.zookeeper.replicaCount | int | `1` | Numer of Zookeeper replicas in the ZK cluster |
| tolerations | list | `[]` |  |

  [License]: https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=flat
  [1]: https://opensource.org/licenses/Apache-2.0
  [Chat on Gitter]: https://badges.gitter.im/gitterHQ/gitter.svg
  [2]: https://gitter.im/keitaroinc/docker-ckan

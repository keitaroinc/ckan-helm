CKAN Helm Chart
==========

[![License][]][1][![Chat on Gitter][]][2]

[License]: https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=flat
[1]: https://opensource.org/licenses/Apache-2.0
[Chat on Gitter]: https://badges.gitter.im/gitterHQ/gitter.svg
[2]: https://gitter.im/keitaroinc/docker-ckan

A Helm chart for CKAN

Current chart version is `v4.0.5`

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
```

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://keitaro-charts.storage.googleapis.com | postgresql | 16.7.27 |
| https://keitaro-charts.storage.googleapis.com | redis | 23.0.2 |
| https://keitaro-charts.storage.googleapis.com | solr | 9.6.10 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| CkanDBName | string | `"ckan_default"` | Variable for name of the database used by CKAN |
| CkanDBPass | string | `"pass"` | Variable for password for the CKAN database owner |
| CkanDBUser | string | `"ckan_default"` | Variable for username for the owner of the CKAN database |
| DBDeploymentName | string | `"postgres"` | Variable for name override for postgres deployment |
| DBHost | string | `"postgres"` | Variable for name of headless svc from postgres deployment or external host connection string |
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
| ZookeeperName | string | `"zookeeper"` | Variable for name override for zookeeper deployment |
| affinity | object | `{}` | Pod affinity |
| ckan.activityStreamsEmailNotifications | string | `"true"` | Set to true to enable email notifications for activity streams for this to work smtp must be configured |
| ckan.ckanPlugins | string | `"envvars activity image_view text_view datatables_view datastore xloader"` | List of plugins to be used by the instance |
| ckan.ckanext_xloader_site_url | string | `"http://ckan:80"` | URL for the xloader extension to use for file uploads |
| ckan.container_debug | string | `"false"` |  |
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
| ckan.debug | string | `"false"` | Set to true to enable debug mode in CKAN |
| ckan.extraEnv | list | `[]` | An array to add extra environment variables For example: extraEnv:   - name: FOO     value: "bar"  |
| ckan.issues.sendEmailNotifications | string | `"true"` |  |
| ckan.liveness.failureThreshold | int | `6` | Failure threshold for the liveness probe |
| ckan.liveness.initialDelaySeconds | int | `10` | Initial delay for the liveness probe |
| ckan.liveness.periodSeconds | int | `10` | Check interval for the liveness probe |
| ckan.liveness.timeoutSeconds | int | `15` | Timeout interval for the liveness probe |
| ckan.locale.default | string | `"en"` |  |
| ckan.locale.offered | string | `"en"` |  |
| ckan.maintenanceMode | string | `"false"` | Set to true to disable CKAN from starting and serve a maintenance page |
| ckan.psql.initialize | bool | `true` | Flag whether to initialize the PostgreSQL instance with the provided users and databases |
| ckan.psql.masterDatabase | string | `"postgres"` | PostgreSQL database for the master user |
| ckan.psql.masterPassword | string | `"pass"` | PostgreSQL master user password |
| ckan.psql.masterUser | string | `"postgres"` | PostgreSQL master username |
| ckan.psql.runOnAzure | bool | `false` | Set to true to run on Azure (if true wont run on anything other then azure) set to false to run on other platforms   |
| ckan.readiness.failureThreshold | int | `6` | Failure threshold for the readiness probe |
| ckan.readiness.initialDelaySeconds | int | `10` | Inital delay seconds for the readiness probe |
| ckan.readiness.periodSeconds | int | `10` | Check interval for the readiness probe |
| ckan.readiness.timeoutSeconds | int | `15` | Timeout interval for the readiness probe |
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
| ckan.spatialBackend | string | `"solr"` | Spatial backend to be used by the instance |
| ckan.storagePath | string | `"/app/data"` | Storage path to be used by the instance |
| ckan.sysadminApiToken | string | `"replace_this_with_generated_api_token_for_sysadmin"` | CKAN system admin API token Needs to be generated via the CKAN UI and replaced after initial deployment |
| ckan.sysadminEmail | string | `"admin@domain.com"` | CKAN system admin email |
| ckan.sysadminName | string | `"ckan_admin"` | CKAN system admin username |
| ckan.sysadminPassword | string | `"PasswordHere"` | CKAN system admin password |
| ckan.upload_enabled | string | `"true"` | Set to "true" to enable file uploads in CKAN |
| ckan.uwsg_num | string | `"2"` |  |
| ckan.workers | list | `[{"command":["ckan","-c","/app/production.ini","jobs","worker","default"],"name":"default","replicas":1},{"command":["ckan","-c","/app/production.ini","jobs","worker","bulk"],"name":"bulk","replicas":1},{"command":["ckan","-c","/app/production.ini","jobs","worker","priority"],"name":"priority","replicas":1}]` | Configuration for CKAN worker deployments for custom workers add additional entries to the array |
| fullnameOverride | string | `"ckan"` | Override for full chart name |
| hpa.cpuTargetAverageUtilization | int | `80` | HPA CPU target utilization |
| hpa.enabled | bool | `false` | Enable horizontal pod autoscaler |
| hpa.maxReplicas | int | `5` | Maximum HPA replicas |
| hpa.memoryTargetAverageUtilization | int | `80` | HPA memory target utilization |
| hpa.minReplicas | int | `1` | Minimum HPA replicas |
| hpa.sessions.session_type | string | `"redis"` | HPA session type |
| image.initContainer.pullPolicy | string | `"IfNotPresent"` |  |
| image.initContainer.repository | string | `"busybox"` | Image for init containers |
| image.initContainer.tag | string | `"stable"` |  |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy   |
| image.repository | string | `"keitaro/ckan"` | CKAN Docker image repository |
| image.tag | string | `"2.11.4"` | CKAN Docker image tag |
| image.testConnection.pullPolicy | string | `"IfNotPresent"` |  |
| image.testConnection.repository | string | `"busybox"` | Image for test connection jobs |
| image.testConnection.tag | string | `"stable"` |  |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{}` | Ingress annotations |
| ingress.className | string | `""` | Ingress class name     |
| ingress.enabled | bool | `false` | Enable ingress |
| ingress.hosts | list | `[{"host":"chart-example.local","paths":[{"path":"/","pathType":"ImplementationSpecific"}]}]` | Ingress hosts |
| ingress.tls | list | `[]` | Ingress TLS configuration         |
| ingressRoute | object | `{"enabled":false,"host":"chart-example.local"}` | Used in conjunction with a Traefik v2 deployment |
| ingressRoute.enabled | bool | `false` | Enable Traefik ingress route |
| ingressRoute.host | string | `"chart-example.local"` | Traefik ingress route host |
| labels.ckan | list | `[]` | Custom labels for CKAN deployment |
| labels.enabled | bool | `false` | Enable custom labels |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` | Node selector |
| podSecurityContext | object | `{"runAsGroup":92,"runAsUser":92}` | Pod security context |
| postgresql.auth.database | string | `"ckan_default"` |  |
| postgresql.auth.password | string | `"pass"` |  |
| postgresql.auth.postgresPassword | string | `"pass"` |  |
| postgresql.auth.username | string | `"ckan_default"` |  |
| postgresql.enabled | bool | `true` | Flag to control whether to deploy PostgreSQL |
| postgresql.fullnameOverride | string | `"postgres"` | Name override for the PostgreSQL deployment |
| postgresql.global.security.allowInsecureImages | bool | `true` |  |
| postgresql.persistence.size | string | `"1Gi"` | Size of the PostgreSQL pvc |
| pvc.accessmode | string | `"ReadWriteOnce"` | Access mode for PVC |
| pvc.enabled | bool | `true` | Enable persistent volume claim |
| pvc.size | string | `"1Gi"` | Size of the PVC |
| pvc.storageClassName | string | `"standard"` | Storage class for PVC |
| redis.architecture | string | `"standalone"` | Redis architecture for standalone or replication versions |
| redis.auth.enabled | bool | `false` | Enable or disable redis password auth |
| redis.auth.password | string | `nil` | The password of redis if auth is enabled |
| redis.auth.sentinel | bool | `false` | Enables or disables passwords for sentinels |
| redis.enabled | bool | `true` | Flag to control whether to deploy Redis |
| redis.fullnameOverride | string | `"redis"` | Name override for the redis deployment |
| redis.global.security.allowInsecureImages | bool | `true` |  |
| redis.master.persistence.enabled | bool | `false` | Enable redis volume claim |
| redis.master.persistence.size | string | `"1Gi"` | Size of the volume claim |
| redis.replicaCount | int | `1` |  |
| replicaCount | int | `1` | Number of CKAN pods to deploy |
| resources | object | `{}` | Resource requests/limits |
| securityContext | object | `{"allowPrivilegeEscalation":false}` | Container security context |
| service.port | int | `80` | Service port |
| service.type | string | `"ClusterIP"` | Type of the service created for the CKAN pod |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `false` | Specifies whether a service account should be created |
| serviceAccount.name | string | `nil` | The name of the service account to use. If not set and create is true, a name is generated using the fullname template |
| solr.auth.adminPassword | string | `"pass"` | The password of the solr admin user |
| solr.auth.adminUsername | string | `"admin"` |  |
| solr.auth.enabled | bool | `true` | Enable or disable auth (if auth is disabled solr-init cant upload the configset/schema.xml for ckan) |
| solr.collection | string | `nil` | the name of the collection created by solr  since we are creating one with solr-init this needs to be blank |
| solr.collectionReplicas | int | `0` | Number of replicas for each SOLR shard |
| solr.collectionShards | int | `0` | Number of shards for the SOLR collection |
| solr.enabled | bool | `true` | Flag to control whether to deploy SOLR |
| solr.fullnameOverride | string | `"solr"` | Name override for the SOLR deployment |
| solr.global.imagePullSecrets | list | `[]` |  |
| solr.global.imageRegistry | string | `""` |  |
| solr.global.security.allowInsecureImages | bool | `true` |  |
| solr.global.storageClass | string | `""` |  |
| solr.initialize.configsetName | string | `"ckanConfigSet"` | Name of the config set used for initializing |
| solr.initialize.container_debug | string | `"false"` |  |
| solr.initialize.enabled | bool | `true` | Flag whether to initialize the SOLR instance with the provided collection name |
| solr.initialize.maxShardsPerNode | int | `10` | Maximum shards per node |
| solr.initialize.numShards | int | `2` | Number of shards for the SOLR collection |
| solr.initialize.replicationFactor | int | `1` | Number of replicas for each SOLR shard |
| solr.replicaCount | int | `1` | Number of SOLR instances in the cluster |
| solr.volumeClaimTemplates.storageSize | string | `"5Gi"` | Size of Solr PVC |
| solr.zookeeper.enabled | bool | `true` |  |
| solr.zookeeper.fullnameOverride | string | `"zookeeper"` |  |
| solr.zookeeper.global.security.allowInsecureImages | bool | `true` |  |
| solr.zookeeper.image.digest | string | `""` |  |
| solr.zookeeper.image.registry | string | `"public.ecr.aws"` |  |
| solr.zookeeper.image.repository | string | `"bitnami/zookeeper"` |  |
| solr.zookeeper.image.tag | string | `"3.9.3-debian-12-r22"` |  |
| solr.zookeeper.persistence.size | string | `"1Gi"` | Size of ZK PVC |
| solr.zookeeper.replicaCount | int | `1` | Numer of Zookeeper replicas in the ZK cluster |
| tolerations | list | `[]` | Pod tolerations |

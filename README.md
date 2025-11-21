CKAN Helm Chart
==========

[![License][]][1][![Chat on Gitter][]][2]

A Helm chart for CKAN

Current chart version is `4.0.4`

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


## Chart Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://charts.bitnami.com/bitnami | postgresql | 16.7.27 |
| https://charts.bitnami.com/bitnami | redis | 23.0.2 |
| https://charts.bitnami.com/bitnami | solr | 9.6.10 |

## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| replicaCount | int | `1` | Number of CKAN pods to deploy |
| image.repository | string | `"keitaro/ckan"` | CKAN Docker image repository |
| image.tag | string | `"2.11.3"` | CKAN Docker image tag |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.testConnection.repository | string | `"busybox"` | Image for test connection jobs |
| image.initContainer.repository | string | `"busybox"` | Image for init containers |
| imagePullSecrets | list | `[]` | List of image pull secrets |
| nameOverride | string | `""` | Override for chart name |
| fullnameOverride | string | `"ckan"` | Override for full chart name |
| pvc.enabled | bool | `true` | Enable persistent volume claim |
| pvc.size | string | `"1Gi"` | Size of the PVC |
| pvc.storageClassName | string | `"standard"` | Storage class for PVC |
| pvc.accessmode | string | `"ReadWriteOnce"` | Access mode for PVC |
| DBDeploymentName | string | `"postgres"` | Name override for postgres deployment |
| RedisName | string | `"redis"` | Name override for redis deployment |
| SolrName | string | `"solr"` | Name override for solr deployment |
| ZookeeperName | string | `"zookeeper"` | Name override for zookeeper deployment |
| DBHost | string | `"postgres"` | Name of headless svc from postgres deployment or external host connection string |
| MasterDBName | string | `"postgres"` | Name of the master user database in PostgreSQL |
| MasterDBUser | string | `"postgres"` | Master user name for PostgreSQL |
| MasterDBPass | string | `"pass"` | Password for the master user in PostgreSQL |
| CkanDBName | string | `"ckan_default"` | Name of the database used by CKAN |
| CkanDBUser | string | `"ckan_default"` | Username for the owner of the CKAN database |
| CkanDBPass | string | `"pass"` | Password for the CKAN database owner |
| DatastoreDBName | string | `"datastore_default"` | Name of the database used by Datastore |
| DatastoreRWDBUser | string | `"datastorerw"` | Username for the user with write access to the datastore database |
| DatastoreRWDBPass | string | `"pass"` | Password for the datastore database user with write access |
| DatastoreRODBUser | string | `"datastorero"` | Username for the user with read access to the datastore database |
| DatastoreRODBPass | string | `"pass"` | Password for the datastore database user with read access |
| ckan.sysadminName | string | `"ckan_admin"` | CKAN system admin username |
| ckan.sysadminPassword | string | `"PasswordHere"` | CKAN system admin password |
| ckan.sysadminApiToken | string | `"replace_this_with_generated_api_token_for_sysadmin"` | CKAN system admin API token |
| ckan.sysadminEmail | string | `"admin@domain.com"` | CKAN system admin email |
| ckan.siteTitle | string | `"Site Title here"` | Site title for the instance |
| ckan.siteId | string | `"site-id-here"` | Site id |
| ckan.siteUrl | string | `"http://localhost:5000"` | Url for the CKAN instance |
| ckan.ckanPlugins | string | `"envvars activity image_view text_view datatables_view datastore xloader"` | List of plugins to be used by the instance |
| ckan.storagePath | string | `"/app/data"` | Storage path to be used by the instance |
| ckan.activityStreamsEmailNotifications | string | `"true"` | Enable email notifications for activity streams |
| ckan.debug | string | `"false"` | Set to true to enable debug mode in CKAN |
| ckan.container_debug | string | `"false"` | Set entrypoint to sleep infinity for debugging |
| ckan.uwsg_num | string | `"2"` | Number of uswgi workers CKAN will start |
| ckan.maintenanceMode | string | `"false"` | Set to true to serve a maintenance page |
| ckan.ckanext_xloader_site_url | string | `"http://ckan:80"` | URL for the xloader extension to use for file uploads |
| ckan.workers | list | See values.yaml | Configuration for CKAN worker deployments |
| ckan.psql.runOnAzure | bool | `false` | Set to true to run on Azure |
| ckan.psql.initialize | bool | `true` | Flag to initialize PostgreSQL instance |
| ckan.psql.masterUser | string | `"postgres"` | PostgreSQL master username |
| ckan.psql.masterPassword | string | `"pass"` | PostgreSQL master user password |
| ckan.psql.masterDatabase | string | `"postgres"` | PostgreSQL database for the master user |
| ckan.solr | string | `"http://solr-headless:8983/solr/ckancollection"` | Location of SOLR collection |
| ckan.redis | string | `"redis://redis-headless:6379/0"` | Location of the Redis service |
| ckan.spatialBackend | string | `"solr"` | Spatial backend to be used |
| ckan.locale.offered | string | `"en"` | Offered locale |
| ckan.locale.default | string | `"en"` | Default locale |
| ckan.smtp.server | string | `"smtpServerURLorIP:port"` | SMTP server address |
| ckan.smtp.user | string | `"smtpUser"` | SMTP user |
| ckan.smtp.password | string | `"smtpPassword"` | SMTP password |
| ckan.smtp.mailFrom | string | `"postmaster@domain.com"` | SMTP mail from address |
| ckan.smtp.tls | string | `"enabled"` | Enable SMTP TLS |
| ckan.smtp.starttls | string | `"true"` | Enable SMTP STARTTLS |
| ckan.issues.sendEmailNotifications | string | `"true"` | Enable issue email notifications |
| ckan.extraEnv | list | `[]` | Extra environment variables |
| ckan.readiness.initialDelaySeconds | int | `10` | Initial delay for readiness probe |
| ckan.readiness.periodSeconds | int | `10` | Period for readiness probe |
| ckan.readiness.failureThreshold | int | `6` | Failure threshold for readiness probe |
| ckan.readiness.timeoutSeconds | int | `10` | Timeout for readiness probe |
| ckan.liveness.initialDelaySeconds | int | `10` | Initial delay for liveness probe |
| ckan.liveness.periodSeconds | int | `10` | Period for liveness probe |
| ckan.liveness.failureThreshold | int | `6` | Failure threshold for liveness probe |
| ckan.liveness.timeoutSeconds | int | `10` | Timeout for liveness probe |
| ckan.db.ckanDbUrl | string | `"postgres"` | PostgreSQL server for CKAN DB |
| ckan.db.ckanDbName | string | `"ckan_default"` | CKAN database name |
| ckan.db.ckanDbUser | string | `"ckan_default"` | CKAN database user |
| ckan.db.ckanDbPassword | string | `"pass"` | CKAN database password |
| ckan.datastore.RwDbUrl | string | `"postgres"` | PostgreSQL server for Datastore RW DB |
| ckan.datastore.RwDbName | string | `"datastore_default"` | Datastore RW database name |
| ckan.datastore.RwDbUser | string | `"datastorerw"` | Datastore RW database user |
| ckan.datastore.RwDbPassword | string | `"pass"` | Datastore RW database password |
| ckan.datastore.RoDbUrl | string | `"postgres"` | PostgreSQL server for Datastore RO DB |
| ckan.datastore.RoDbName | string | `"datastore_default"` | Datastore RO database name |
| ckan.datastore.RoDbUser | string | `"datastorero"` | Datastore RO database user |
| ckan.datastore.RoDbPassword | string | `"pass"` | Datastore RO database password |
| serviceAccount.create | bool | `false` | Specifies whether a service account should be created |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.name | string | `nil` | Name of the service account to use |
| labels.enabled | bool | `false` | Enable custom labels |
| labels.ckan | object | `{}` | Custom labels for CKAN deployment |
| podSecurityContext | object | `{}` | Pod security context |
| securityContext | object | `{}` | Container security context |
| service.type | string | `"ClusterIP"` | Type of the service created for CKAN pod |
| service.port | int | `80` | Service port |
| ingress.enabled | bool | `false` | Enable ingress |
| ingress.annotations | object | `{}` | Ingress annotations |
| ingress.className | string | `""` | Ingress class name |
| ingress.hosts | list | `[chart-example.local]` | Ingress hosts |
| ingress.tls | list | `[]` | Ingress TLS configuration |
| ingressRoute.enabled | bool | `false` | Enable Traefik ingress route |
| ingressRoute.host | string | `"chart-example.local"` | Traefik ingress route host |
| resources | object | `{}` | Resource requests/limits |
| nodeSelector | object | `{}` | Node selector |
| tolerations | list | `[]` | Pod tolerations |
| affinity | object | `{}` | Pod affinity |
| hpa.enabled | bool | `false` | Enable horizontal pod autoscaler |
| hpa.minReplicas | int | `1` | Minimum HPA replicas |
| hpa.maxReplicas | int | `5` | Maximum HPA replicas |
| hpa.cpuTargetAverageUtilization | int | `80` | HPA CPU target utilization |
| hpa.memoryTargetAverageUtilization | int | `80` | HPA memory target utilization |
| hpa.sessions.session_type | string | `redis` | HPA session type |
| redis.enabled | bool | `true` | Enable Redis deployment |
| redis.fullnameOverride | string | `"redis"` | Redis deployment name override |
| redis.replicaCount | int | `1` | Redis replica count |
| redis.global.security.allowInsecureImages | bool | `true` | Allow insecure images for Redis |
| redis.architecture | string | `"standalone"` | Redis architecture |
| redis.master.persistence.enabled | bool | `false` | Enable Redis master persistence |
| redis.master.persistence.size | string | `"1Gi"` | Redis master persistence size |
| redis.auth.enabled | bool | `false` | Enable Redis password authentication |
| redis.auth.sentinel | bool | `false` | Enable Redis sentinel authentication |
| redis.auth.password | string | `""` | Redis password |
| solr.enabled | bool | `true` | Enable Solr deployment |
| solr.global.imageRegistry | string | `""` | Solr image registry |
| solr.global.imagePullSecrets | list | `[]` | Solr image pull secrets |
| solr.global.storageClass | string | `""` | Solr storage class |
| solr.global.security.allowInsecureImages | bool | `true` | Allow insecure images for Solr |
| solr.auth.enabled | bool | `true` | Enable Solr authentication |
| solr.auth.adminUsername | string | `"admin"` | Solr admin username |
| solr.auth.adminPassword | string | `"pass"` | Solr admin password |
| solr.collection | string | `""` | Solr collection name |
| solr.collectionShards | int | `0` | Number of Solr collection shards |
| solr.collectionReplicas | int | `0` | Number of Solr collection replicas |
| solr.fullnameOverride | string | `"solr"` | Solr deployment name override |
| solr.replicaCount | int | `1` | Solr replica count |
| solr.volumeClaimTemplates.storageSize | string | `"5Gi"` | Solr PVC size |
| solr.initialize.enabled | bool | `true` | Enable Solr initialization |
| solr.initialize.container_debug | string | `"false"` | Set entrypoint to sleep infinity for debugging solr-init |
| solr.initialize.numShards | int | `2` | Number of Solr shards |
| solr.initialize.replicationFactor | int | `1` | Number of Solr replicas per shard |
| solr.initialize.maxShardsPerNode | int | `10` | Max shards per Solr node |
| solr.initialize.configsetName | string | `"ckanConfigSet"` | Solr configset name |
| solr.zookeeper.enabled | bool | `true` | Enable Zookeeper deployment |
| solr.zookeeper.replicaCount | int | `1` | Zookeeper replica count |
| solr.zookeeper.fullnameOverride | string | `"zookeeper"` | Zookeeper deployment name override |
| solr.zookeeper.persistence.size | string | `"1Gi"` | Zookeeper PVC size |
| solr.zookeeper.global.security.allowInsecureImages | bool | `true` | Allow insecure images for Zookeeper |
| solr.zookeeper.image.registry | string | `"public.ecr.aws"` | Zookeeper image registry |
| solr.zookeeper.image.repository | string | `"bitnami/zookeeper"` | Zookeeper image repository |
| solr.zookeeper.image.tag | string | `"3.9.3-debian-12-r22"` | Zookeeper image tag |
| solr.zookeeper.image.digest | string | `""` | Zookeeper image digest |
| postgresql.enabled | bool | `true` | Enable PostgreSQL deployment |
| postgresql.persistence.size | string | `"1Gi"` | PostgreSQL PVC size |
| postgresql.global.security.allowInsecureImages | bool | `true` | Allow insecure images for PostgreSQL |
| postgresql.fullnameOverride | string | `"postgres"` | PostgreSQL deployment name override |
| postgresql.auth.postgresPassword | string | `"pass"` | PostgreSQL admin password |
| postgresql.auth.username | string | `"ckan_default"` | PostgreSQL custom user |
| postgresql.auth.password | string | `"pass"` | PostgreSQL custom user password |
| postgresql.auth.database | string | `"ckan_default"` | PostgreSQL custom database |

  [License]: https://img.shields.io/badge/license-Apache--2.0-blue.svg?style=flat
  [1]: https://opensource.org/licenses/Apache-2.0
  [Chat on Gitter]: https://badges.gitter.im/gitterHQ/gitter.svg
  [2]: https://gitter.im/keitaroinc/docker-ckan

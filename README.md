ckan-chart
==========
A Helm chart for CKAN

Current chart version is `0.1.0`



## Chart Requirements

| Repository | Name | Version |
|------------|------|---------|
| file://dependency-charts/datapusher | datapusher | 1.0.0 |
| https://kubernetes-charts-incubator.storage.googleapis.com/ | solr | 1.4.0 |
| https://kubernetes-charts.storage.googleapis.com/ | minio | 5.0.27 |
| https://kubernetes-charts.storage.googleapis.com/ | postgresql | 8.6.4 |
| https://kubernetes-charts.storage.googleapis.com/ | redis | 10.5.6 |

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
| S3FileStoreAccessKey | string | `"minio_admin"` | AWS access key |
| S3FileStoreBucketName | string | `"ckan"` | AWS bucket name |
| S3FileStoreHostName | string | `"http://minio:9000"` | Bucket host name |
| S3FileStoreRegionName | string | `"minio"` | Bucket region name |
| S3FileStoreSecretKey | string | `"minio_pass"` | AWS secret key |
| S3FileStoreSignatureVersion | string | `"s3v4"` | S3 signature version |
| S3FileStoreStoragePath | string | `"ckan_storage"` | S3 storage path |
| SolrName | string | `"solr"` | Variable for name override for solr deployment |
| affinity | object | `{}` |  |
| ckan.activityStreamsEmailNotifications | string | `"true"` |  |
| ckan.ckanPlugins | string | `"envvars s3filestore image_view text_view recline_view datastore datapusher"` | List of plugins to be used by the instance |
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
| ckan.debug | string | `"true"` |  |
| ckan.extraEnv | list | `[]` | An array to add extra environment variables For example: extraEnv:   - name: FOO     value: "bar" |
| ckan.issues.sendEmailNotifications | string | `"true"` |  |
| ckan.liveness.failureThreshold | int | `6` | Failure threshold for the liveness probe |
| ckan.liveness.initialDelaySeconds | int | `10` | Initial delay for the liveness probe |
| ckan.liveness.periodSeconds | int | `10` | Check interval for the liveness probe |
| ckan.liveness.timeoutSeconds | int | `10` | Timeout interval for the liveness probe |
| ckan.locale.default | string | `"en"` |  |
| ckan.locale.offered | string | `"en"` |  |
| ckan.psql.initialize | bool | `true` | Flag whether to initialize the PostgreSQL instance with the provided users and databases |
| ckan.psql.masterDatabase | string | `"postgres"` | PostgreSQL database for the master user |
| ckan.psql.masterPassword | string | `"pass"` | PostgreSQL master user password |
| ckan.psql.masterUser | string | `"postgres"` | PostgreSQL master username |
| ckan.readiness.failureThreshold | int | `6` | Failure threshold for the readiness probe |
| ckan.readiness.initialDelaySeconds | int | `10` | Inital delay seconds for the readiness probe |
| ckan.readiness.periodSeconds | int | `10` |  |
| ckan.readiness.timeoutSeconds | int | `10` | Timeout interval for the readiness probe |
| ckan.redis | string | `"redis://redis-headless:6379/0"` | Location of the Redis service to be used by the CKAN instance |
| ckan.s3filestore.awsAccessKeyId | string | `"minio_admin"` | AWS access key |
| ckan.s3filestore.awsBucketName | string | `"ckan"` | S3 bucket name |
| ckan.s3filestore.awsSecretAccessKey | string | `"minio_pass"` | AWS secret key |
| ckan.s3filestore.awsStoragePath | string | `"ckan_storage"` | S3 storage path |
| ckan.s3filestore.hostName | string | `"http://minio:9000"` | S3 host name |
| ckan.s3filestore.regionName | string | `"minio"` | S3 region name |
| ckan.s3filestore.signatureVersion | string | `"s3v4"` | S3 signature version |
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
| ckan.sysadminEmail | string | `"admin@domain.com"` | CKAN system admin email |
| ckan.sysadminName | string | `"ckan_admin"` | CKAN system admin username |
| ckan.sysadminPassword | string | `"PasswordHere"` | CKAN system admin password |
| datapusher.enabled | bool | `true` | Flag to control whether to deploy the datapusher |
| datapusher.fullnameOverride | string | `"datapusher"` | Name override for the datapusher deployment |
| fullnameOverride | string | `"ckan"` |  |
| image.pullPolicy | string | `"Always"` |  |
| image.repository | string | `"keitaro/ckan"` |  |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0].host | string | `"chart-example.local"` |  |
| ingress.hosts[0].paths | list | `[]` |  |
| ingress.tls | list | `[]` |  |
| minio.accessKey | string | `"minio_admin"` | Access key for minio |
| minio.defaultBucket.enabled | bool | `true` | Flag to control whether to create default bucket |
| minio.defaultBucket.name | string | `"ckan"` | Name of the default Minio bucket |
| minio.defaultBucket.policy | string | `"upload"` | Policy of the default Minio bucket |
| minio.enabled | bool | `true` | Flag to control whether to deploy Minio |
| minio.fullnameOverride | string | `"minio"` | Name override for the Minio deployment |
| minio.persistence.size | string | `"5Gi"` | Size of the Minio PVC |
| minio.secretKey | string | `"minio_pass"` | Secret key for minio |
| minio.service.port | int | `9000` | The port used by the Mino service |
| minio.service.type | string | `"NodePort"` | The service type of the Minio service |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| postgresql.enabled | bool | `true` | Flag to control whether to deploy PostgreSQL |
| postgresql.existingSecret | string | `"postgrescredentials"` | Name of existing secret that holds passwords for PostgreSQL |
| postgresql.fullnameOverride | string | `"postgres"` | Name override for the PostgreSQL deployment |
| postgresql.persistence.size | string | `"1Gi"` | Size of the PostgreSQL pvc |
| postgresql.pgPass | string | `"pass"` | Password for the master PostgreSQL user. Feeds into the `postgrescredentials` secret that is provided to the PostgreSQL chart |
| pvc.enabled | string | `"false"` |  |
| pvc.size | string | `"1Gi"` |  |
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
| solr.zookeeper.replicaCount | int | `1` | Numer of Zookeeper replicas in the ZK cluster |
| solr.zookeeper.persistence.size | string | `"1Gi"` | Size of ZK PVC |
| tolerations | list | `[]` |  |

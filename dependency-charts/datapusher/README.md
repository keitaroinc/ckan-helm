datapusher
==========
CKAN Datapusher helm chart

Current chart version is `1.0.0`





## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| datapusher.chunkSize | string | `"16384"` | Size of chunks of the data that is being downloaded in bytes |
| datapusher.datapusherRewriteResources | string | `"True"` | Enable or disable (boolean) whether datapusher should rewrite resources uploaded to CKAN's filestore, since datapusher takes the CKAN Site URL value for generating the resource URL. Default: False |
| datapusher.datapusherRewriteUrl | string | `"http://ckan"` |  |
| datapusher.datapusherSslVerify | string | `"False"` | Enable or disable (boolean) verification of SSL when trying to get resources. Default: True |
| datapusher.downloadTimeout | string | `"30"` | Timeout limit of the download request |
| datapusher.insertRows | string | `"250"` | Number of rows to take from the data and upload them as chunks to datastore |
| datapusher.maxContentLength | string | `"10485760"` | Maximum size of content to be uploaded in bytes. |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"keitaro/ckan-datapusher"` |  |
| image.tag | string | `"0.0.17"` |  |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0].host | string | `"chart-example.local"` |  |
| ingress.hosts[0].paths | list | `[]` |  |
| ingress.tls | list | `[]` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `8000` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `nil` |  |
| tolerations | list | `[]` |  |

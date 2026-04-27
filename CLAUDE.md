# Claude Code Instructions — ckan-helm

## What This Repo Is
A Helm chart for deploying a self-contained CKAN (open data portal) instance on Kubernetes, including all dependencies (PostgreSQL, Solr, Redis) as sub-charts sourced from the Keitaro Helm repo.

## Structure
- `Chart.yaml` — chart metadata, version (`v4.0.7`), app version (`2.11.3`), and sub-chart dependency declarations
- `Chart.lock` — locked dependency versions
- `values.yaml` — all configurable values: CKAN settings, database credentials, Solr/Redis config, ingress, HPA, workers
- `templates/` — Kubernetes manifest templates (Deployment, Service, Ingress, IngressRoute, PVC, HPA, CronJob, init Jobs, Secrets, ConfigMaps, ServiceAccount)
- `templates/tests/` — Helm test connection pod
- `solr-init/` — Python script and Solr configset (schema, solrconfig.xml) used by the solr-init Job to create the CKAN collection
- `.github/workflows/` — CI pipelines: chart packaging and upload to GCS (`main.yml`), helm-docs generation, YAML linting, Trivy security scan, manual release

## Making Changes
- **Local install/upgrade:** `helm dep up` first (to pull sub-charts), then `helm install <release> .` or `helm upgrade <release> .` with a custom values file
- **Dependencies:** declared in `Chart.yaml`; update versions there and run `helm dep update` to regenerate `Chart.lock`
- **Releasing:** push a git tag — the `main.yml` workflow packages the chart and uploads it to the `gs://keitaro-charts` GCS bucket, then rebuilds `index.yaml`
- **README:** generated from `README.md.gotmpl` via `helm-docs`; run `helm-docs` locally or let the CI workflow regenerate it

## Conventions
- YAML anchors are used heavily in `values.yaml` to share credential values (e.g. `&MasterDBPass`, `&CkanDBUser`) — reference with `*` aliases rather than duplicating literals
- `fullnameOverride: "ckan"` is set by default; changing it will rename all resources
- The `sysadminApiToken` in `values.yaml` must be replaced with a real token generated via the CKAN UI after the first deployment
- Both standard Kubernetes `ingress` and Traefik `ingressRoute` are supported — only enable one at a time
- Worker deployments are defined as an array under `ckan.workers`; add entries to create additional worker Deployments
- The psql-init and solr-init Jobs run once on install; set `ckan.psql.initialize: false` and `solr.initialize.enabled: false` when targeting an already-initialised external database/Solr

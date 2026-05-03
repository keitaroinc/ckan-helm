# Using Custom CKAN Image from GitHub Container Registry

This repository automatically builds a custom CKAN Docker image with scheming and DCAT extensions and publishes it to GitHub Container Registry (ghcr.io).

---

## 🐳 Image Details

**Registry**: `ghcr.io`
**Image**: `ghcr.io/mpparsley/ckan-helm/ckan-custom`
**Base**: `keitaro/ckan:2.11.4`

### Included Extensions

- ✅ **ckanext-scheming** 3.1.0 - Custom metadata schemas
- ✅ **ckanext-dcat** 2.4.2 - RDF/DCAT metadata export
- ✅ **rdflib** 7.0.0 - Python RDF library

### Available Tags

| Tag | Description | When Updated |
|-----|-------------|--------------|
| `latest` | Latest build from master branch | On every push to master |
| `2.11.4-scheming3.1-dcat2.4` | Semantic version tag | On push to master |
| `master-<sha>` | Git commit SHA | On every push to master |
| `pr-<number>` | Pull request preview | On PR creation/update |

---

## 🔑 Authentication

### Public Access (Default)

The images are public by default. No authentication needed:

```bash
docker pull ghcr.io/mpparsley/ckan-helm/ckan-custom:latest
```

### Private Access (If Repository is Private)

If the repository is private, you need a GitHub Personal Access Token (PAT):

1. **Create a PAT** with `read:packages` scope:
   - Go to https://github.com/settings/tokens
   - Generate new token (classic)
   - Select `read:packages` scope
   - Copy the token

2. **Login to ghcr.io**:
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
   ```

3. **Pull the image**:
   ```bash
   docker pull ghcr.io/mpparsley/ckan-helm/ckan-custom:latest
   ```

---

## 📦 Using in Helm Deployment

### Option 1: Public Image (No Secret Needed)

Update your `values-openshift.yaml`:

```yaml
image:
  repository: ghcr.io/mpparsley/ckan-helm/ckan-custom
  tag: "2.11.4-scheming3.1-dcat2.4"
  pullPolicy: Always

# Plugin configuration is already baked into the image
# But you can override via extraEnv if needed
ckan:
  # Plugins are already configured in the image
  # ckanPlugins will be read from production.ini in the image

  # Add scheming configuration
  extraEnv:
    - name: CKAN__SCHEMING__DATASET_SCHEMAS
      value: "ckanext.scheming:ckan_dataset.yaml /app/schemas/dataset_schema.yaml"

    - name: CKAN__SCHEMING__PRESETS
      value: "ckanext.scheming:presets.json ckanext.dcat.schemas:presets.yaml"

    - name: CKANEXT__DCAT__RDF_PROFILES
      value: "euro_dcat_ap_2 euro_dcat_ap"

    - name: CKANEXT__DCAT__ENABLE_RDF_ENDPOINTS
      value: "true"
```

Deploy:

```bash
helm upgrade ckan . -f values-openshift.yaml -n d09-open-data-qa
```

### Option 2: Private Image (With Pull Secret)

If your repository is private, create an image pull secret:

```bash
# Create pull secret in OpenShift
kubectl create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_GITHUB_PAT \
  --docker-email=YOUR_EMAIL \
  -n d09-open-data-qa
```

Update `values-openshift.yaml`:

```yaml
image:
  repository: ghcr.io/mpparsley/ckan-helm/ckan-custom
  tag: "2.11.4-scheming3.1-dcat2.4"
  pullPolicy: Always

imagePullSecrets:
  - name: ghcr-pull-secret

ckan:
  extraEnv:
    - name: CKAN__SCHEMING__DATASET_SCHEMAS
      value: "/app/schemas/dataset_schema.yaml"
    - name: CKANEXT__DCAT__ENABLE_RDF_ENDPOINTS
      value: "true"
```

---

## 🚀 GitHub Actions Workflow

### Automatic Builds

The workflow (`.github/workflows/build-custom-ckan-image.yaml`) automatically builds on:

- ✅ Push to `master` or `main` branch
- ✅ Pull requests (preview builds)
- ✅ Manual trigger via GitHub UI
- ✅ Changes to `Dockerfile.custom` or `schemas/`

### Manual Trigger

You can manually trigger a build:

1. Go to **Actions** tab in GitHub
2. Select **Build and Push Custom CKAN Image**
3. Click **Run workflow**
4. Optional: Add a tag suffix (e.g., `-test`, `-beta`)

### Build Cache

The workflow uses GitHub Actions cache to speed up builds:
- First build: ~5-10 minutes
- Subsequent builds: ~2-3 minutes (with cache)

---

## 🔍 Verifying the Image

### Check Available Tags

```bash
# List all tags (requires gh CLI)
gh api /user/packages/container/ckan-helm%2Fckan-custom/versions \
  --jq '.[].metadata.container.tags[]' | sort -u
```

### Inspect Image

```bash
# Pull and inspect
docker pull ghcr.io/mpparsley/ckan-helm/ckan-custom:latest

# Check installed extensions
docker run --rm ghcr.io/mpparsley/ckan-helm/ckan-custom:latest \
  pip list | grep ckanext

# Expected output:
# ckanext-dcat        2.4.2
# ckanext-scheming    3.1.0

# Check plugins configuration
docker run --rm ghcr.io/mpparsley/ckan-helm/ckan-custom:latest \
  grep "ckan.plugins" /app/production.ini

# Expected output:
# ckan.plugins = envvars activity image_view text_view datatables_view datastore xloader scheming_datasets dcat dcat_json_interface structured_data
```

### Test Locally

```bash
# Run locally with docker-compose
docker run -p 5000:5000 \
  -e CKAN_SQLALCHEMY_URL=postgresql://ckan:pass@postgres/ckan \
  -e CKAN_SOLR_URL=http://solr:8983/solr/ckan \
  -e CKAN_REDIS_URL=redis://redis:6379/0 \
  ghcr.io/mpparsley/ckan-helm/ckan-custom:latest
```

---

## 📝 Making Changes

### Updating Extensions

1. **Edit `Dockerfile.custom`**:
   ```dockerfile
   ENV SCHEMING_VERSION="3.2.0"  # Update version
   ENV DCAT_VERSION="2.5.0"      # Update version
   ```

2. **Update semantic tag in workflow** (`.github/workflows/build-custom-ckan-image.yaml`):
   ```yaml
   type=raw,value=2.11.4-scheming3.2-dcat2.5
   ```

3. **Commit and push**:
   ```bash
   git add Dockerfile.custom .github/workflows/build-custom-ckan-image.yaml
   git commit -m "Update extensions: scheming 3.2.0, DCAT 2.5.0"
   git push origin master
   ```

4. **GitHub Actions will automatically build** and push the new image

### Adding New Extensions

1. **Edit `Dockerfile.custom`**:
   ```dockerfile
   ENV HARVEST_VERSION="1.5.6"

   RUN uv pip install --system \
       ckanext-scheming==${SCHEMING_VERSION} \
       ckanext-dcat==${DCAT_VERSION} \
       ckanext-harvest==${HARVEST_VERSION} \
       rdflib==${RDFLIB_VERSION}
   ```

2. **Update plugin list**:
   ```dockerfile
   ENV CKAN__PLUGINS="envvars ... scheming_datasets dcat harvest ckan_harvester"
   ```

3. **Commit, push, and let GitHub Actions build**

---

## 🔒 Security Considerations

### Image Scanning

The workflow includes basic security practices:
- ✅ Uses official GitHub Actions
- ✅ Minimal base image (Alpine-based)
- ✅ Non-root user (ckan user)
- ✅ Version pinning for all extensions

### Recommended: Add Vulnerability Scanning

You can add Trivy scanning to the workflow:

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload Trivy results to GitHub Security
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

---

## 🆘 Troubleshooting

### Build Fails on GitHub Actions

**Check the Actions logs**:
1. Go to **Actions** tab
2. Click on the failed workflow
3. Check the **Build and push Docker image** step

Common issues:
- **Schema file missing**: Ensure `schemas/dataset_schema.yaml` exists
- **Permission denied**: Check repository permissions for GITHUB_TOKEN
- **Rate limit**: Wait a few minutes and retry

### Image Pull Fails in OpenShift

**Error**: `ErrImagePull` or `ImagePullBackOff`

**Solutions**:

1. **Check image exists**:
   ```bash
   docker pull ghcr.io/mpparsley/ckan-helm/ckan-custom:latest
   ```

2. **For private repos, create pull secret**:
   ```bash
   kubectl create secret docker-registry ghcr-pull-secret \
     --docker-server=ghcr.io \
     --docker-username=YOUR_USERNAME \
     --docker-password=YOUR_PAT \
     -n d09-open-data-qa
   ```

3. **Add secret to values**:
   ```yaml
   imagePullSecrets:
     - name: ghcr-pull-secret
   ```

### Plugins Not Loading

**Check pod logs**:
```bash
kubectl logs -n d09-open-data-qa deployment/ckan | grep -i "plugin\|error"
```

**Common issues**:
- Plugin not in CKAN__PLUGINS list
- Missing configuration (check extraEnv)
- Extension dependencies not installed

---

## 📊 Monitoring Builds

### GitHub Actions Badge

Add to your README:

```markdown
[![Build Custom CKAN Image](https://github.com/MPParsley/ckan-helm/actions/workflows/build-custom-ckan-image.yaml/badge.svg)](https://github.com/MPParsley/ckan-helm/actions/workflows/build-custom-ckan-image.yaml)
```

### Check Latest Build

```bash
# Using gh CLI
gh run list --workflow=build-custom-ckan-image.yaml --limit 5

# Check specific run
gh run view <run-id>
```

---

## 🎯 Quick Start for QA Deployment

```bash
# 1. Ensure schemas directory exists
mkdir -p schemas
# (dataset_schema.yaml should already be there)

# 2. Commit and push Dockerfile.custom
git add Dockerfile.custom schemas/
git commit -m "Add custom CKAN image with scheming and DCAT"
git push origin master

# 3. Wait for GitHub Actions to build (~5-10 minutes)
# Check: https://github.com/MPParsley/ckan-helm/actions

# 4. Update values-openshift.yaml
cat >> values-openshift.yaml <<EOF
image:
  repository: ghcr.io/mpparsley/ckan-helm/ckan-custom
  tag: "2.11.4-scheming3.1-dcat2.4"
  pullPolicy: Always

ckan:
  extraEnv:
    - name: CKAN__SCHEMING__DATASET_SCHEMAS
      value: "/app/schemas/dataset_schema.yaml"
    - name: CKANEXT__DCAT__RDF_PROFILES
      value: "euro_dcat_ap_2"
    - name: CKANEXT__DCAT__ENABLE_RDF_ENDPOINTS
      value: "true"
EOF

# 5. Deploy to QA
helm upgrade ckan . -f values-openshift.yaml -n d09-open-data-qa

# 6. Verify deployment
kubectl get pods -n d09-open-data-qa -l app.kubernetes.io/name=ckan
kubectl logs -n d09-open-data-qa deployment/ckan | grep "Loading plugin"
```

---

## 📚 Resources

- [GitHub Container Registry Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [CKAN Extension Development](https://docs.ckan.org/en/latest/extensions/index.html)
- [CKAN Scheming](https://github.com/ckan/ckanext-scheming)
- [CKAN DCAT](https://github.com/ckan/ckanext-dcat)

---

**Ready to deploy!** 🚀

The custom image will be automatically built and pushed to GitHub Container Registry on every push to master.

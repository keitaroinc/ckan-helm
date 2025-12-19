############
### MAIN ###
############
FROM ghcr.io/keitaroinc/ckan:2.11.4

# CKAN extension source code URLs
#ENV ACME_GIT_URL="https://github.com/myghorg/ckanext-acme.git"
#ENV ACME_GIT_VERSION="0.4.2"
#ENV ACME_REQUIREMENTS_URL="https://raw.githubusercontent.com/myghorg/ckanext-acme/refs/tags/${ACME_GIT_VERSION}/requirements.txt"

### Scheming ###
ENV SCHEMING_GIT_URL="https://github.com/ckan/ckanext-scheming.git"
ENV SCHEMING_GIT_VERSION="release-3.1.0"

### Harvest (required by dcat_rdf_harvester) ###
ENV HARVEST_GIT_URL="https://github.com/ckan/ckanext-harvest.git"
ENV HARVEST_GIT_VERSION="v1.6.2"
ENV HARVEST_REQUIREMENTS_URL="https://raw.githubusercontent.com/ckan/ckanext-harvest/refs/tags/${HARVEST_GIT_VERSION}/requirements.txt"

### DCAT ###
ENV DCAT_GIT_URL="https://github.com/ckan/ckanext-dcat.git"
ENV DCAT_GIT_VERSION="v2.4.2"
ENV DCAT_REQUIREMENTS_URL="https://raw.githubusercontent.com/ckan/ckanext-dcat/refs/tags/${DCAT_GIT_VERSION}/requirements.txt"

### Pages ###
#ENV PAGES_GIT_URL="https://github.com/ckan/ckanext-pages.git"
#ENV PAGES_GIT_VERSION="master"

# Add the custom extensions to the plugins list
ENV CKAN__PLUGINS="envvars activity image_view text_view datatables_view datastore xloader scheming_datasets harvest dcat dcat_rdf_harvester structured_data"

# Switch to the root user
USER root

# Install and enable the custom extensions
    # Install necessary system packages with apk 
RUN apk add --no-cache libffi-dev && \
    # Install the CKAN extension and any requirements using uv
    uv pip install --system git+${SCHEMING_GIT_URL}@${SCHEMING_GIT_VERSION} && \
    uv pip install --system git+${HARVEST_GIT_URL}@${HARVEST_GIT_VERSION} && \
    uv pip install --system -r ${HARVEST_REQUIREMENTS_URL} && \
    uv pip install --system git+${DCAT_GIT_URL}@${DCAT_GIT_VERSION} && \
    # Install any other required python packages
    uv pip install --system requests && \
    # Create schemas directory
    mkdir -p ${APP_DIR}/schemas && \
    chown -R ckan:ckan ${APP_DIR}/schemas && \
    # Update plugin configuration
    ckan config-tool ${APP_DIR}/production.ini "ckan.plugins = ${CKAN__PLUGINS}" && \
    ckan config-tool ${APP_DIR}/production.ini "scheming.dataset_schemas = file://${APP_DIR}/schemas/dcat_ap_stadgent.yaml" && \
    ckan config-tool ${APP_DIR}/production.ini "scheming.presets = ckanext.scheming:presets.json ckanext.dcat.schemas:presets.yaml" && \
    ckan config-tool ${APP_DIR}/production.ini "ckanext.dcat.rdf.profiles = euro_dcat_ap_3" && \
    chown -R ckan:ckan /app && \
    # Remove uv cache
    rm -rf /app/cache

# Copy custom Stad Gent DCAT schema
COPY --chown=ckan:ckan schemas/dcat_ap_stadgent.yaml ${APP_DIR}/schemas/

# Switch to the ckan user
USER ckan

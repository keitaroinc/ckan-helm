"""
Copyright (c) 2020 Keitaro AB

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import shutil
import os
import sys
import requests
import json
import time


solr_admin_username = os.environ.get('SOLR_ADMIN_USERNAME', '')
solr_admin_password = os.environ.get('SOLR_ADMIN_PASSWORD', '')

def check_solr_connection(solr_url, retry=None):
    print('\nCheck_solr_connection...')
    sys.stdout.flush()

    if retry is None:
        retry = 60
    elif retry == 0:
        print('Giving up ...')
        sys.exit(1)

    try:
        response = requests.get(solr_url, auth=(solr_admin_username, solr_admin_password), timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        print('Unable to connect to solr...retrying.')
        sys.stdout.flush()
        import time
        time.sleep(30)
        check_solr_connection(solr_url, retry=retry - 1)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        print('Unable to connect to solr...retrying.')
        sys.stdout.flush()
        import time
        time.sleep(30)
        check_solr_connection(solr_url, retry=retry - 1)
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        print('Unable to connect to solr...retrying.')
        sys.stdout.flush()
        import time
        time.sleep(30)
        check_solr_connection(solr_url, retry=retry - 1)
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        print('Unable to connect to solr...retrying.')
        sys.stdout.flush()
        import time
        time.sleep(30)
        check_solr_connection(solr_url, retry=retry - 1)
    else:
        print("OK")


def prepare_configset(cfset_name):
    print("\nPreparing configset...")

    # Copy configset files from configmap volume into rw volume
    # and include schema.xml from ckan src
    base_dir = "/app/data/solr-configset"
    shutil.copytree("/app/solr-configset",base_dir)
    shutil.copyfile("/app/src/ckan/ckan/config/solr/schema.xml",
                    os.path.join(base_dir, "schema.xml"))
    
    # Create lang folder so we have same structure as helm chart folder
    target_folder = os.path.join(base_dir, "lang")

    # Create target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    # list of filenames to exclude
    exclude_files = {"protwords.txt", "stopwords.txt", "synonyms.txt"}

    # Move all .txt files in base_dir to target_folder
    for filename in os.listdir(base_dir):
        if filename.endswith(".txt") and filename not in exclude_files:
            src = os.path.join(base_dir, filename)
            dst = os.path.join(target_folder, filename)
            shutil.move(src, dst)

    # Ensure the configset directory exists
    if not os.path.exists("/app/data/solr-configset"):
        print("Error: 'solr-configset' directory does not exist")
        sys.exit(2)

    # Create zip
    zip_path = '/app/data/temp_configset.zip'
    try:
        print("Creating Configset ZIP file...")
        shutil.make_archive('/app/data/temp_configset', 'zip', '/app/data/solr-configset')
    except Exception as e:
        print(f"Failed to create ZIP: {e}")
        sys.exit(2)

    # Upload configSet
    url = f"{solr_url}/solr/admin/configs?action=UPLOAD&name={cfset_name}"
    print(f"Uploading ZIP file to Zookeeper via Solr: {url}")

    try:
        with open(zip_path, 'rb') as f:
            data = f.read()
        res = requests.post(
            url,
            data=data,
            auth=(solr_admin_username, solr_admin_password),
            headers={'Content-Type': 'application/octet-stream'},
            timeout=10  # avoid hanging indefinitely
        )
        # Raise for HTTP errors (4xx/5xx)
        res.raise_for_status()
        print("Configset uploaded successfully.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {res.status_code} - {res.text}")
        # If configset already exists, exit successfully
        if res.status_code == 400 and 'already exists' in res.text:
            print("Configset already exists. Will be used for creating the collection.")
        elif res.status_code == 409:
            print("Configset already exists. Will be used for creating the collection.")
        else:
            print("Failed to upload configset due to HTTP error.")
            sys.exit(3)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        sys.exit(3)
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
        sys.exit(3)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(3)


def create_solr_collection(name, cfset_name, num_shards, repl_factor,
                           max_shards_node):
    time.sleep(5)
    print("\nCreating Solr collection based on uploaded configset...")
    url = solr_url + '/solr/admin/collections?action=CREATE&name=' + name
    url = url + '&numShards=' + num_shards
    url = url + '&replicationFactor=' + repl_factor
    url = url + '&maxShardsPerNode=' + max_shards_node
    url = url + '&collection.configName=' + cfset_name
    print("Trying: " + url)
    try:
        res = requests.post(url, 
                            auth=(solr_admin_username,solr_admin_password), timeout=10)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {res.status_code} - {res.text}")
        # If collection already exists, exit successfully
        if res.status_code == 400 and 'already exists' in res.text:
            print("Collection already exists. Exiting successfully.")
            sys.exit(0)
        print("Failed to create collection due to HTTP error.")
        sys.exit(4)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        sys.exit(4)
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
        sys.exit(4)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(4)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(4)
    print("OK")


def solr_collection_alreadyexists(solr_url):
    print("\nChecking if solr collection already exists")
    url = solr_url + '/solr/admin/collections?action=LIST&wt=json'
    print("Trying: " + url)
    try:
        res = requests.post(url,
                            auth=(solr_admin_username,solr_admin_password), timeout=10)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {res.status_code} - {res.text}")
        print("Failed to list collections due to HTTP error.")
        sys.exit(5)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        sys.exit(5)
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
        sys.exit(5)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(5)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(5)
    response_dict = json.loads(res.text)
    if collection_name in response_dict['collections']:
        print('Collection exists. Aborting.')
        sys.exit(0)

    print('Collection does not exist. OK...')


if (os.environ.get('CKAN_SOLR_URL', '') == ''):
    print("Error: CKAN_SOLR_URL env var not defined. Exiting...")
    sys.exit(1)

# Get the values for the initializing Solr from env
collection_name = os.environ.get('CKAN_SOLR_URL', '').split('/')[-1]
protocol = os.environ.get('CKAN_SOLR_URL', '').split('/')[0]
solr_url = protocol + "//" + os.environ.get('CKAN_SOLR_URL', '').split('/')[2]
num_shards = os.environ.get('CKAN_SOLR_INIT_NUMSHARDS', '2')
repl_factor = os.environ.get('CKAN_SOLR_INIT_REPLICATIONFACTOR', '1')
max_shards_node = os.environ.get('CKAN_SOLR_INIT_MAXSHARDSPERNODE', '10')
cfset_name = os.environ.get('CKAN_SOLR_INIT_CONFIGSETNAME', 'ckanConfigSet')

print("Preparing Solr...")
print("Solr host: " + solr_url)
print("Collection name: " + collection_name)

check_solr_connection(solr_url)
solr_collection_alreadyexists(solr_url)
prepare_configset(cfset_name)
create_solr_collection(collection_name, cfset_name, num_shards,
                       repl_factor, max_shards_node)
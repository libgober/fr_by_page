import os
import json
import requests
from tqdm import tqdm
import random

random.seed(1)
selection_probability = 0.01
# Define the directory containing the JSON files
directory = 'package_summaries'

# Define the API key
api_key = 'bnsOg5reiXtijPW74z7FZyJeVkMMtqf89vrvJDy9'

# Ensure the download directories exist
os.makedirs('mods_files', exist_ok=True)
os.makedirs('pdf_files', exist_ok=True)

# Function to download a file from a given URL
def download_file(url, dest_folder, filename, api_key):
    if not url:
        return
    file_path = os.path.join(dest_folder, filename)
    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"File {file_path} already exists. Skipping download.")
        return
    headers = {'accept': 'application/json'}
    response = requests.get(f"{url}?api_key={api_key}", headers=headers)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download {url} with status code: {response.status_code}")
        if os.path.exists(file_path):
            os.remove(file_path)  # Delete the file if the download failed

# Loop over the JSON files in the directory
for filename in tqdm(os.listdir(directory)):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Get the packageId for naming the files
            package_id = data.get('packageId')
            # Get the links for mods and pdf
            mods_link = data.get('download', {}).get('modsLink')
            pdf_link = data.get('download', {}).get('pdfLink')
            # Download the files with the packageId as the filename
            download_file(mods_link, 'mods_files', f"{package_id}.mods.xml", api_key)
            if random.random() < selection_probability:
                download_file(pdf_link, 'pdf_files', f"{package_id}.pdf", api_key)

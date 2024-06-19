import pandas as pd
import requests
import os
import json
from tqdm import tqdm

# Read the packages DataFrame from CSV
packages = pd.read_csv('packages.csv')

# Define the headers and API key
headers = {
    'accept': 'application/json'
}
api_key = 'bnsOg5reiXtijPW74z7FZyJeVkMMtqf89vrvJDy9'

# Ensure the package_summaries directory exists
os.makedirs('package_summaries', exist_ok=True)

# Loop over the DataFrame and fetch the links
for index, row in tqdm(packages.iterrows(), total=packages.shape[0]):
    package_link = row['packageLink']
    package_id = row['packageId']
    file_path = os.path.join('package_summaries', f"{package_id}.json")
    
    # Check if the file already exists
    if not os.path.exists(file_path):
        response = requests.get(f"{package_link}?api_key={api_key}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Save the JSON data to a file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            print(f"Request failed for {package_link} with status code: {response.status_code}")

# Verify that all intended files were downloaded
missing_files = []
for index, row in packages.iterrows():
    package_id = row['packageId']
    file_path = os.path.join('package_summaries', f"{package_id}.json")
    if not os.path.exists(file_path):
        missing_files.append(package_id)

# Print missing files if any
if missing_files:
    print("The following files were not downloaded:")
    for file in missing_files:
        print(file)
else:
    print("All files were successfully downloaded.")

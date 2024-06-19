#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:19:50 2024

@author: blibgober
"""


import requests
from tqdm import tqdm
import pandas as pd
# Define the parameters
lastModifiedStartDate = "1900-01-01T01:01:01Z"
api_key = 'bnsOg5reiXtijPW74z7FZyJeVkMMtqf89vrvJDy9'
base_url = 'https://api.govinfo.gov/collections/FR/{lastModifiedStartDate}'.format(lastModifiedStartDate=lastModifiedStartDate)

# Define the parameters and headers
params = {
    'pageSize': '1000',
    'offsetMark': '*',
    'api_key': api_key
}
headers = {
    'accept': 'application/json'
}

# Function to fetch data with pagination
def fetch_data(url, headers, params):
    all_data = []

    # Initial request to get the total count
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        total_count = data['count']
        all_data.extend(data.get('packages', []))

        # Progress bar setup
        pbar = tqdm(total=total_count, initial=len(all_data))
        pbar.update(len(all_data))
        # Continue fetching remaining pages
        while data['nextPage'] is not None:
            next_page = data['nextPage']
            response = requests.get(next_page,params={'api_key': api_key})
            if response.status_code == 200:
                data = response.json()
                new_packages = data.get('packages', [])
                all_data.extend(new_packages)
                pbar.update(len(new_packages))
            else:
                print(f"Request failed with status code: {response.status_code}")
                break

        pbar.close()
    else:
        print(f"Initial request failed with status code: {response.status_code}")

    if response.json()['count'] == len(all_data):
        print("Success! Got all expected packages")
    return all_data

# Fetch the data
data = fetch_data(base_url, headers, params)

# Print or process the data as needed
package_data = pd.DataFrame(data)
package_data.to_csv("packages.csv")

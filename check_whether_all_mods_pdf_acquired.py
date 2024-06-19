#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:31:33 2024

@author: blibgober
"""


import os
import json

# Define the directory containing the JSON files
json_directory = 'package_summaries'
mods_directory = 'mods_files'
pdf_directory = 'pdf_files'

# Lists to track missing files
missing_mods_files = []
missing_pdf_files = []

# Loop over the JSON files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Get the packageId for naming the files
            package_id = data.get('packageId')
            # Define expected file paths
            mods_file_path = os.path.join(mods_directory, f"{package_id}.mods.xml")
            pdf_file_path = os.path.join(pdf_directory, f"{package_id}.pdf")
            # Check if the mods file exists
            if not os.path.exists(mods_file_path):
                missing_mods_files.append(package_id)
            # Check if the pdf file exists
            if not os.path.exists(pdf_file_path):
                missing_pdf_files.append(package_id)

# Print missing files if any
if missing_mods_files:
    print("The following mods files are missing:")
    for package_id in missing_mods_files:
        print(package_id)
else:
    print("All mods files are present.")

if missing_pdf_files:
    print("The following pdf files are missing:")
    for package_id in missing_pdf_files:
        print(package_id)
else:
    print("All pdf files are present.")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:32:19 2024

@author: blibgober
"""


import os
import json
import requests
from tqdm import tqdm
import PyPDF2
import parsel
import re
# Define the directories
json_directory = 'package_summaries'
mods_directory = 'mods_files'
pdf_directory = 'pdf_files'
output_directory = 'split_pdfs'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to split PDF based on page ranges
def split_pdf(pdf_path, output_dir, page_ranges):
    pdf_reader = PyPDF2.PdfFileReader(pdf_path)
    for start_page, end_page, page_type in page_ranges:
        pdf_writer = PyPDF2.PdfFileWriter()
        current_page = 0
        
        for page_num in range(start_page, end_page + 1):
            pdf_writer.addPage(pdf_reader.getPage(current_page))
            current_page += 1
        
        output_path = os.path.join(output_dir, f'{os.path.basename(pdf_path).replace(".pdf", "")}_{start_page}-{end_page}.pdf')
        with open(output_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
            
            
            
# Helper function to convert Roman numerals to integers
def roman_to_int(s):
    roman_numerals = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000,
        'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900
    }
    i = 0
    num = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i+2] in roman_numerals:
            num += roman_numerals[s[i:i+2]]
            i += 2
        else:
            num += roman_numerals[s[i]]
            i += 1
    return num

# Function to parse MODS file for page ranges
import parsel

# Function to parse MODS file for page ranges
def parse_mods(mods_path):
    # Load the MODS XML file
    with open(mods_path, 'r') as file:
        mods_xml = file.read()
    
    # Parse the XML using parsel
    selector = parsel.Selector(mods_xml, type='xml')
    selector.remove_namespaces()
    
    # Extract page ranges
    page_ranges = []
    for part in selector.xpath("//part[@type='issue']"):
        start_page_text = part.xpath('.//start/text()').get()
        end_page_text = part.xpath('.//end/text()').get()
        
        # Convert page numbers to integers
        start_page = int(start_page_text)
        end_page = int(end_page_text)
        
        page_ranges.append((start_page, end_page))
    
    return page_ranges



# Loop over the JSON files in the directory
for filename in tqdm(os.listdir(json_directory)):
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
            # Check if both files exist
            if os.path.exists(mods_file_path) and os.path.exists(pdf_file_path):
                # Parse the MODS file to get the page ranges
                page_ranges = parse_mods(mods_file_path)
                # Split the PDF based on the parsed page ranges
                split_pdf(pdf_file_path, output_directory, page_ranges)
            else:
                print(f"Missing files for {package_id}: mods or pdf file not found.")

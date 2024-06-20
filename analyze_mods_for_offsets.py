import os
import pandas as pd
import parsel

# Directory containing the XML files
directory = 'mods_files'

# List to store results
results = []

# Loop over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.xml'):
        filepath = os.path.join(directory, filename)
        
        # Read the XML file
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse the XML content using parsel and remove namespaces
        selector = parsel.Selector(text=content, type='xml')
        selector.remove_namespaces()
        
        # Check for printPageRange tag and offset attribute
        print_page_range = selector.xpath('//printPageRange')
        has_print_page_range = len(print_page_range) > 0
        offset = print_page_range.xpath('@offset').get() if has_print_page_range else None
        
        # Append result to list
        results.append({
            'Filename': filename,
            'HasPrintPageRange': has_print_page_range,
            'Offset': offset
        })

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Save the DataFrame to a CSV file
df.to_csv('print_page_range_results.csv', index=False)

print("Results saved to print_page_range_results.csv")

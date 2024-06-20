import pandas as pd
import re
from datetime import datetime

# Read the CSV file
df = pd.read_csv('print_page_range_results.csv')

# Function to extract date from filename
def extract_date(filename):
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    if match:
        return datetime.strptime(match.group(), '%Y-%m-%d')
    return None

# Apply the function to extract dates and add them to the DataFrame
df['Date'] = df['Filename'].apply(extract_date)

# Ensure the DataFrame is sorted by Date
df = df.sort_values(by='Date')

# Identify contiguous ranges based on the presence of printPageRange
def find_contiguous_ranges(df):
    ranges = []
    start_date = df.iloc[0]['Date']
    current_has_print_page_range = df.iloc[0]['HasPrintPageRange']
    for i in range(1, len(df)):
        if df.iloc[i]['HasPrintPageRange'] != current_has_print_page_range:
            end_date = df.iloc[i - 1]['Date']
            ranges.append((start_date, end_date, current_has_print_page_range))
            start_date = df.iloc[i]['Date']
            current_has_print_page_range = df.iloc[i]['HasPrintPageRange']
    # Append the last range
    ranges.append((start_date, df.iloc[-1]['Date'], current_has_print_page_range))
    return ranges

# Find the contiguous ranges
contiguous_ranges = find_contiguous_ranges(df)

# Print the results
print("Contiguous date ranges:")
for start, end, has_print_page_range in contiguous_ranges:
    range_type = 'with' if has_print_page_range else 'without'
    print(f"{start} to {end} - {range_type} printPageRange")

# Optionally, you can save these ranges to a new DataFrame and then to a CSV
ranges_df = pd.DataFrame(contiguous_ranges, columns=['Start Date', 'End Date', 'HasPrintPageRange'])
ranges_df['HasPrintPageRange'] = ranges_df['HasPrintPageRange'].map({True: 'with', False: 'without'})
ranges_df.to_csv('contiguous_date_ranges.csv', index=False)

print("Contiguous date ranges saved to contiguous_date_ranges.csv")

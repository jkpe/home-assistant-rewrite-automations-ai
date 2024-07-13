import json
import os

# Function to split JSON into multiple files
def split_json_into_files(json_file, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    for item in data:
        file_name = f"{item['id']}.json"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as out_file:
            json.dump(item, out_file, indent=4)
        print(f"Created file: {file_path}")

# Specify the input JSON file
input_json_file = 'automations.json'
# Specify the output directory
output_directory = 'output-split-json'

# Run the function
split_json_into_files(input_json_file, output_directory)
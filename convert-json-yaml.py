import os
import json
import yaml

# Function to convert JSON files to a single YAML file with specified top-level keys
def convert_json_to_yaml(input_dir, output_file):
    yaml_data = []

    # Define the order of keys to be maintained
    key_order = ['id', 'alias', 'description']

    # Loop through each file in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)

                # Check for use_blueprint key and remove specific keys if it exists
                if 'use_blueprint' in data:
                    keys_to_skip = {'trigger', 'condition', 'action'}
                else:
                    keys_to_skip = set()
                
                # Create an ordered dictionary to maintain key order and skip certain keys if necessary
                ordered_data = {key: data.get(key) for key in key_order}
                
                if not keys_to_skip:
                    # Add optional keys only if they should not be skipped
                    optional_keys = ['trigger', 'condition', 'action']
                    for key in optional_keys:
                        ordered_data[key] = data.get(key)

                # Add any remaining keys that are not in the predefined order or skipped list 
                for key in data:
                    if (key not in ordered_data) and (key not in keys_to_skip):
                        ordered_data[key] = data[key]
                
                yaml_data.append(ordered_data)
    
    # Write the combined data to the YAML file with explicit start indicator and default flow style off
    with open(output_file, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)
    
    print(f"Created YAML file: {output_file}")

# Specify the input directory and output file
input_directory = 'output'
output_yaml_file = 'output.yaml'

# Run the function
convert_json_to_yaml(input_directory, output_yaml_file)
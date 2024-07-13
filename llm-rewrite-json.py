import os
import json
import subprocess
import argparse

PROCESSED_FILES_LOG = 'processed_files.log'

def call_llm(file_path):
    """Calls the LLM to get the new alias and description."""
    command = f'cat {file_path} | llm -m gpt-4o --no-stream -s "Based on what this Home Assistant automation does and how it works, rewrite a new Alias and Description for it. In your response just give me the updated alias and description. Respond with JSON objects."'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error calling LLM: {result.stderr}")
        return ""
    
    return result.stdout.strip()

def clean_response(response):
    """Cleans the LLM response by removing any Markdown code fences and single quotes."""
    if response.startswith("```json") and response.endswith("```"):
        response = response[7:-3].strip()
    elif response.startswith("```") and response.endswith("```"):
        response = response[3:-3].strip()

    # Remove leading/trailing single quotes
    if response.startswith("'") and response.endswith("'"):
        response = response[1:-1].strip()

    # Replace any internal single quotes with double quotes for valid JSON parsing
    return response.replace("'", '')

def update_json_file(input_file_path, output_file_path, new_data):
    """Updates the JSON file with the new alias and description."""
    with open(input_file_path, 'r') as file:
        data = json.load(file)

    # Assuming the new data contains keys "alias" and "description"
    data['alias'] = new_data.get('alias', data.get('alias'))
    data['description'] = new_data.get('description', data.get('description'))

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_processed_files():
    """Reads processed files from log."""
    if not os.path.exists(PROCESSED_FILES_LOG):
        return set()
    
    with open(PROCESSED_FILES_LOG, 'r') as file:
        return set(line.strip() for line in file)

def mark_as_processed(file_name):
    """Marks a file as processed by adding its name to the log."""
    with open(PROCESSED_FILES_LOG, 'a') as file:
        file.write(file_name + '\n')

def process_directory(directory):
     """Processes all JSON files in a directory."""
     processed_files = get_processed_files()
     
     for filename in os.listdir(directory):
         if filename.endswith(".json") and filename not in processed_files:
             input_file_path = os.path.join(directory, filename)
             output_file_path = os.path.join('output', filename)
             print(f'Processing {input_file_path}')
             
             # Call LLM to get updated alias and description
             llm_response = call_llm(input_file_path)
             
             if not llm_response:
                 print(f"No valid response from LLM for {filename}")
                 continue
             
             # Clean up possible Markdown code fences from the LLM's response
             cleaned_response = clean_response(llm_response)

             try:
                 new_data = json.loads(cleaned_response)
                 update_json_file(input_file_path, output_file_path, new_data)
                 mark_as_processed(filename)
                 print(f'Successfully updated {input_file_path} -> {output_file_path}')
             except json.JSONDecodeError as e:
                 print(f'Failed to decode JSON response for {filename}: {e}\nResponse was: {cleaned_response}')

def process_single_file(file_path):
     """Processes a single JSON file."""
     filename = os.path.basename(file_path)
     processed_files = get_processed_files()
     
     if filename in processed_files:
         print(f"{filename} has already been processed.")
         return

     output_file_path = os.path.join('output', filename)
     print(f'Processing {file_path}')
     
     # Call LLM to get updated alias and description
     llm_response = call_llm(file_path)

     if not llm_response:
         print(f"No valid response from LLM for {filename}")
         return

     # Clean up possible Markdown code fences from the LLM's response
     cleaned_response = clean_response(llm_response)

     try:
         new_data = json.loads(cleaned_response)
         update_json_file(file_path, output_file_path, new_data)
         mark_as_processed(filename)
         print(f'Successfully updated {file_path} -> {output_file_path}')
     except json.JSONDecodeError as e:
         print(f'Failed to decode JSON response for {filename}: {e}\nResponse was: {cleaned_response}')


if __name__ == "__main__":
     parser = argparse.ArgumentParser(description='Process Home Assistant automation JSON files.')
     
     group = parser.add_mutually_exclusive_group(required=True)
     
     group.add_argument('-d', '--directory', help='Directory containing JSON files to process')
     group.add_argument('-f', '--file', help='Specific JSON file to process')
     
     args = parser.parse_args()
     
     if args.directory:
         process_directory(args.directory)
         
     elif args.file:
         process_single_file(args.file)      
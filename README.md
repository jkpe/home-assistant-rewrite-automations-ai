# Rewrite your Home Assistant automations titles and descriptions using a LLM (Large Language Model) such as GPT-4o

Required:

- [llm](https://llm.datasette.io/en/stable/)
- OpenAI API key or Claude would likely work too

## Convert automations.yaml to JSON

`yq eval -o=json automations.yaml > automations.json`

## Split each automation into it's own JSON file

`python3 json_split.py`

## Rewrite using an LLM

Call GPT-4o using [llm](https://llm.datasette.io/en/stable/) to rewrite the alias and description for each automation

`python3 llm-rewrite-json.py -d output-split-json`

usage: llm-rewrite-json.py [-h] (-d DIRECTORY | -f FILE)

 The script will iterate over each JSON file in directory `output-split-json` and for each file succesfully processed add it's file name to `processed_files.log`, this allows you to run the script again on the same directory of files if the llm fails to process an individual automation.

## Convert the rewritten JSON back to YAML

 `python3 convert-json-yaml.py`

This script will merge all json files back into one `automations.yaml` that can be imported back into Home Assistant.

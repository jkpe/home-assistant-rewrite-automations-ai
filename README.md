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

 The script is designed to iterate over each JSON file in the `output-split-json` directory and send it to GPT-4o for processing. GPT-4o will analyze each automation, determine its function, and generate a new title (alias) and description for it. Successfully processed files will be logged in `processed_files.log.` This logging mechanism allows you to rerun the script on the same directory if the LLM fails to process any individual automation.

 The script works by piping each JSON into GPT-4o with a custom prompt

`cat {file} | llm -m gpt-4o --no-stream -s "Based on what this Home Assistant automation does and how it works, rewrite a new Alias and Description for it. In your response just give me the updated alias and description. Respond with JSON objects."`

## Convert the rewritten JSON back to YAML

 `python3 convert-json-yaml.py`

This script will merge all json files back into one `automations.yaml` that can be imported back into Home Assistant.

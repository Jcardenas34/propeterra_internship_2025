# Propeterra Data Science Internship 2025

# Setup
Initial package creation setup must be done in order for the package to work.
once the repo is pulled, Simply navigate to the folder and run

```
pip install -e .
```
This will then create a package of the code base and make everything in src a module that can be used from the rest of the codebase.

## Prompt creation for manual submission
Functionality to construct a predefined prompt for the models in order to obtain relevant real estate links can be run as follows
the script creates a template document to paste results of the model obtained via web interface. API interface is also available.
although not advised since it does cost model and sources need to be vetted

```
python scripts/submit_query.py -c "Costa Rica" -pn 12 -sp 2 -ns 60 -m gemini_2.5_flash
```
-c: Indicates the country of interest 
```
options any country defined in all_countries.py
```
-ns: Indicates the number of links you instruct the model to return 
-pn: Indicates the prompt to be used
-n: The prompt prototype, defined in prompt_templates.py

## Checking the quality of the links provided by the models.
The links will be provided in a standardized JSON format, of which a 404 scanner can be run over the output log to scan through the links to check their validity.
Drastically reduces the number of links that need to be checked by hand. Example usability is below, navigate to model_output/country and run

```
python ../../scripts/valid_links_multi_file.py -c "Costa Rica" gpt-4.1_Costa_Rica_2025-07-07_prompt_12.txt
```
produces a log of which links failed and which passed, as well as creates separate .json files with clean and dead links for uploading to JIRA


## 100/1000 question submission
Functionality to submit the 100 or 1000 questions from the Propeterra orientation questions excel sheet.
Preprocessing of the 1000 questions sheet needs to be done to be compatible with script

```
python scripts/submit_real_estate_questions.py -c Argentina -m gpt-4.1 -sp 3 -i data/2025_INTERNSHIP_ORIENTATION-100_questions.csv -qn 2
```

here the arguments specify the country of interest (Works for all countries defined in all_countries.py) and using 2 models chatgpt and perplexity models.
given that you have defined their API keys in your .bashrc as OPENAI_API_KEYS_PROPETERRA and PERPLEXITY_API_KEYS_PROPETERRA
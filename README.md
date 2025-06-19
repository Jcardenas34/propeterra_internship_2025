# Propeterra Data Science Internship 2025

## Prompt creation for manual submission
Functionality to construct a predefined prompt for the models in oder to obtain relevant real estate links can be run as follows

```
python scripts/query_model.py -r "Latin America" -ns 10 -n 1
```
-r: Indicates the region of interest, with 
```
options: Latin America, Caribbean, North America, South America, Europe, Africa, Asia, Oceania, Middle East
```
-ns: Indicates the number of links you instruct the model to return 

-n: The prompt prototype, defined in prompt_templates.py
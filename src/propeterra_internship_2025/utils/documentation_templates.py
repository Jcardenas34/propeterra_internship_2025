

class DocumentationTemplate():
    
data_collection_template = f'''
User and Date:
------------------
user: Juan Cardenas
date: {date.today()}

Country:
------------
country: {self.country}

Data sourced using:
----------------------
method: 
model: {self.model}

General Notes:
-----------------------

Prompt:
-----------------------
system_prompt_num: {self.system_prompt_number}
prompt_num: {self.prompt_number}

{self.system_prompt+'\n\n'+self.user_prompt}

Human Sourced Links:
----------------------
num_links:

AI Returned Links:
----------------------
num_viable_ai_links:

'''

real_estate_questions_template = f'''
User and Date:
------------------
user: Juan Cardenas
date: {date.today()}

Country:
------------
country: {self.country}

Data sourced using:
----------------------
method: API
model: {self.model}

General Notes:
-----------------------

Prompt:
-----------------------
system_prompt_num: {self.system_prompt_number}
prompt_num: {self.prompt_number}

{self.system_prompt+'\n\n'+self.user_prompt}

AI Response:
----------------------

'''
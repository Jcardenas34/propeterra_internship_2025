import os
from datetime import date
from openai import OpenAI
from propeterra_internship_2025.utils.user_prompts import user_prompt_dictionary, real_estate_professionals_prompt_dictionary
from propeterra_internship_2025.utils.system_prompts import system_prompt_dictionary


class QueryModel():
    ''' Class to select which model to query '''

    def __init__(self, model:str, country:str, system_prompt:str, user_prompt:str, prompt_number:int, system_prompt_number:int, outfile_comment:str=""):
        self.model = model
        self.country = country
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.prompt_number = prompt_number
        self.system_prompt_number = system_prompt_number
        self.outfile_comment = outfile_comment


        self.supported_models = {"gpt-4.1":  os.environ.get("OPENAI_API_KEY_PROPETERRA"),
                                 "sonar":    os.environ.get("PERPLEXITY_API_KEY_PROPETERRA"),
                                 "sonar-pro":os.environ.get("PERPLEXITY_API_KEY_PROPETERRA"),
                                 "sonar-deep-research":os.environ.get("PERPLEXITY_API_KEY_PROPETERRA"),
                                 "ms_copilot":os.environ.get("MS_COPILOT_API_KEY"),
                                 "mistral":         os.environ.get("MISTRAL_API_KEY"),
                                 "gemini_2.5_flash":os.environ.get("GEMINI_API_KEY"),
                                 "manus":           os.environ.get("MANUS_API_KEY")}


        if model not in self.supported_models:

            raise ValueError("Selected model not in list of supported models.")
            # logging.error("Selected model not in list of supported models.")
        if not user_prompt:
            raise ValueError("Prompt is an empty string, please choose a valid prompt number")
        
    def write_to_file(self, model:str, country:str , response, prompt_number:int):
        ''' Writes the response from the model to a text file. And outputs prompt to console'''
        if not os.path.isdir(f"model_output/{country}"):
            os.mkdir(f"model_output/{country}")
  
        with open(f"model_output/{country}/{model}_{country}_{date.today()}_prompt_{prompt_number}.txt", "a", encoding="utf8") as file:
            file.write(response)
        print(response)

    def write_to_real_estate_questions_file(self, model:str, country:str , response, prompt_number:int, outfile_comment:str):
        ''' Writes the response from the model to a text file. And outputs prompt to console'''
        if not os.path.isdir(f"model_output/{country}"):
            os.mkdir(f"model_output/{country}")

        with open(f"model_output/{country}/{model}_{country}_{date.today()}_real_estate_question_{prompt_number}{outfile_comment}.txt", "a", encoding="utf8") as file:
            file.write(response)

    def initialize_file(self):
        ''' Creates a default template to fill with model submission details for documentation purposes '''
        template = f'''
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
        self.write_to_file(self.model, self.country, template, self.prompt_number)

    def initialize_real_estate_questions_file(self):
        ''' Creates a default template to fill with model submission details for documentation purposes '''
        template = f'''
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
        self.write_to_real_estate_questions_file(self.model, self.country, template, self.prompt_number, self.outfile_comment)



    def query_openai(self, real_estate_questions:bool=False) -> None:
        ''' Will query the selected model and write the output to a text file named {model}_{country}.txt '''

        if "gpt" not in self.model:
            raise TypeError("Model is not an OpenAI Model please select another supported model")

        client = OpenAI(api_key=self.supported_models[self.model])

        # What the model will receive
        messages = [
            {
                "role": "developer",
                "content": ( 
                    self.system_prompt
                ),
            },
            {   
                "role": "user",
                "content": (
                    self.user_prompt
                ),
            },
        ]

        response = client.responses.create(
            model=self.model,
            # tools=[{"type": "web_search_preview"}],
            input=messages,
        )  
        message_text = response.output_text
        
  
        if real_estate_questions:
            self.write_to_real_estate_questions_file(self.model, self.country, message_text, self.prompt_number, self.outfile_comment)
        else:
            self.write_to_file(self.model, self.country, message_text, self.prompt_number)


    def query_perplexity(self, real_estate_questions:bool=False) -> None:
        ''' Will query perplexity's sonar-pro model and produce an output text file named {model}_{country}.txt '''


        # What the model will receive
        # search mode allows for more rigorous searching, returning peer reviewed answers etc. https://docs.perplexity.ai/guides/academic-filter-guide
        messages = [
            {
                "role": "system",
                "content": ( 
                    self.system_prompt
                ),
            },
            {   
                "role": "user",
                "content": (
                    self.user_prompt
                ),
                "search_mode":"academic" 
            },
        ]

        client = OpenAI(api_key=self.supported_models[self.model], base_url="https://api.perplexity.ai")

        # chat completion without streaming
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        message_text = response.choices[0].message.content + "\n\n" + str(response.choices)

        if real_estate_questions:
            self.write_to_real_estate_questions_file(self.model, self.country, message_text, self.prompt_number, self.outfile_comment)
        else:
            self.write_to_file(self.model, self.country, message_text, self.prompt_number)

    def query_model(self, real_estate_questions:bool=False) -> None:
        ''' The overarching that will submit a query to the selected model. '''

        if "gpt" in self.model:
            self.query_openai(real_estate_questions)
        elif "sonar" in self.model:
            self.query_perplexity(real_estate_questions)
        else:
            print("No valid model selected, try again")







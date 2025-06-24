import os
from openai import OpenAI

class QueryModel():
    ''' Class to select which model to query '''

    def __init__(self, model:str, country:str, prompt:str):
        self.model = model
        self.country = country
        self.prompt = prompt

        self.SUPPORTED_MODELS = {"gpt-4.1":os.environ.get("OPENAI_API_KEY"),
                                 "sonar_pro":os.environ.get("PERPLEXITY_API_KEY")}


        if model not in self.SUPPORTED_MODELS.keys():
            raise ValueError("Selected model not in list of supported models.")
            # logging.error("Selected model not in list of supported models.")
        if not prompt:
            raise ValueError("Prompt is an empty string, please choose a valid prompt number")
        
    def write_to_file(self, model:str, country:str , response):
        ''' Writes the response from the model to a text file. And outputs prompt to console'''

        with open(f"model_output/{model}_{country}.txt", "a", encoding="utf8") as file:
            file.write(response)
        print(response)

    def query_openai(self) -> None:
        ''' Will query the selected model and write the output to a text file named {model}_{country}.txt '''

        client = OpenAI(api_key=self.SUPPORTED_MODELS[self.model])
        response = client.responses.create(
            model=self.model,
            tools=[{"type": "web_search_preview"}],
            input=self.prompt
        )  
        
        self.write_to_file(self.model, self.country, response)


    def query_sonar_pro(self) -> None:
        ''' Will query perplexity's sonar-pro model and produce an output text file named {model}_{country}.txt '''


        messages = [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you need to "
                    "Aid the user in the collection of data links regarding the real estate industry."
                    "In various countries that are specified by the user. Your job is to collect links to web pages"
                    "that have data in the form of articles, downloadable spreadsheets, plots, on macro economic trends that"
                    "can affect the housing market, and that could provide insights on the current and future state of the real estate"
                    "indutry in the chosen country."
                ),
            },
            {   
                "role": "user",
                "content": (
                    self.prompt
                ),
            },
        ]

        client = OpenAI(api_key=self.SUPPORTED_MODELS[self.model], base_url="https://api.perplexity.ai")
        # chat completion without streaming
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
        )
        message_text = response.choices[0].message.content
        print(message_text)

        # chat completion with streaming
        # response_stream = client.chat.completions.create(
        #     model="sonar-pro",
        #     messages=messages,
        #     stream=True,
        # )
        # for response in response_stream:
        #     print(response)

        self.write_to_file(self.model, self.country, message_text)


# Original query function that works for chatgpt only
# def query_model(model:str, country:str, prompt:str) -> None:
#     ''' Will query the selected model and write the output to a text file named {model}_{country}.txt '''

#     if model not in SUPPORTED_MODELS.keys():
#         raise ValueError("Selected model not in list of supported models.")
#         # logging.error("Selected model not in list of supported models.")
#     if not prompt:
#         raise ValueError("Prompt is an empty string, please choose a valid prompt number")
    
#     # API key is obtained automatically, set OPENAI_API_KEY env var to your API key
#     client = OpenAI()
#     # client = OpenAI(api_key=SUPPORTED_MODELS[model], base_url="https://api.perplexity.ai")
#     response = client.responses.create(
#         model=model,
#         tools=[{"type": "web_search_preview"}],
#         input=prompt
#     )  
    
#     with open(f"model_output/{model}_{country}.txt", "a", encoding="utf8") as file:
#         file.write(response.output_text)
#     logging.info(f"model output written to {model}_{country}.txt successfully.")
#     print(response.output_text)

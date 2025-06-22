import argparse
from openai import OpenAI
from propeterra_internship_2025.data.all_countries import regions
from propeterra_internship_2025.utils.prompt_templates import Prompt


gpt_model = ["gpt-4.1","o4-mini"]


def call_model(model, country, prompt):

    with open(f"model_output/{model}_{country}.txt", "a", encoding="utf8") as file:

        if model in gpt_model and prompt != "":
            client = OpenAI() # API key is obtained automatically by setting your OPENAI_API_KEY environment variable to your API key
            response = client.responses.create(
                model=model,
                tools=[{"type": "web_search_preview"}],
                input=prompt
            )
            file.write(response.output_text)
            print(response.output_text)
        else:
            print("something went wrong")

def main(args):
    '''
    Iterate over the countries in the region of interest and submit a querey to the
    LLM (Which can be specified) 
    '''
    # Pre-defined Region of interest, can choose
    # region_of_interest = "Latin America"
    region_of_interest = args.region


    # Initialize prompt
    prompt = ""

    # Selecting just 1 country
    if args.country != "":
        prompt = Prompt(num_sources=args.n_sources, country_of_interest=args.country, prompt_num=args.prompt_num).construct_prompt()
        print(prompt, "\n\n")
        call_model(args.model, args.country, prompt)
    else:
        # Loop over all countries in a region
        for country in regions.get(region_of_interest, "North America"):
            prompt = Prompt(num_sources=args.n_sources, country_of_interest=country, prompt_num=args.prompt_num).construct_prompt()
            print(prompt, "\n\n")
            # Not calling model yet, stull testing






if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--region", type=str, default="Latin America", choices=regions.keys(), help="The regions that you want to probe, will loop over all countries in region")
    parser.add_argument("-ns","--n_sources", type=int, default=10, help="The number of links you want to get back from the model")
    parser.add_argument("-pn", "--prompt_num", type=int, default=1, help="The prompt template that you want to submit to the model. List of all prompts is located in 'prompt templates'")
    parser.add_argument("-c", '--country', type=str, default="Mexico", help="Specify a single country you would like to generate a prompt for")
    parser.add_argument("-m", "--model", type=str, default="gpt-4.1", choices=["gpt-4.1","perplexity"], help="The model that you want to query")


    args = parser.parse_args()

    main(args)
import os
import logging
import argparse
from openai import OpenAI
from propeterra_internship_2025.data.all_countries import regions, all_countries
from propeterra_internship_2025.utils.prompt_templates import Prompt, create_prompt
from propeterra_internship_2025.utils.model_query import QueryModel


logging.basicConfig(level=logging.INFO)


def main(args: argparse.Namespace) -> None:
    '''
    Iterate over the countries in the region of interest and submit a query to the
    LLM (Which can be specified) 
    '''
    # Pre-defined Region of interest, can choose

    # region_of_interest = "Latin America"
    region_of_interest = args.region


    # Initialize prompt
    prompt = ""

    # Selecting just 1 country
    if args.country:
        if args.country not in all_countries:
            raise TypeError('Selected country {} not found, maybe typo. Please double check.')
        
        system_prompt, user_prompt = create_prompt(n_sources=args.n_sources,
                               country_of_interest=args.country,
                               prompt_num=args.prompt_num,
                               system_prompt_num=args.system_prompt_num)

        # Feeding the prompt to the query framework to be submitted
        query = QueryModel(args.model, args.country, system_prompt, user_prompt, args.prompt_num, args.system_prompt_num)
        query.initialize_file()
        print(prompt, "\n\n")

        # Submitting the actual query
        # query.query_perplexity()
        
    else:

        countries = regions.get(region_of_interest)
        if not countries:
            raise ValueError(f"Could not find {region_of_interest} in list of regions, please choose from available list of regions.")

        # Loop over all countries in a region
        for country in countries:
            prompt = create_prompt(n_sources=args.n_sources,
                                   country_of_interest=country,
                                   prompt_num=args.prompt_num,
                                   system_prompt_num=args.system_prompt_num)
            
            print(prompt, "\n\n")

            # Not calling model yet, still testing
            continue






if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--region", type=str, default="Latin America", choices=regions.keys(), help="The regions that you want to probe, will loop over all countries in region")
    parser.add_argument("-ns","--n_sources", type=int, default=60, help="The number of links you want to get back from the model")
    parser.add_argument("-pn", "--prompt_num", type=int, default=12, help="The prompt template that you want to submit to the model. List of all prompts is located in 'prompt templates'")
    parser.add_argument("-spn", "--system_prompt_num", type=int, default=2, help="The system prompt template that you want to submit to the model. List of all prompts is located in 'prompt templates'")
    parser.add_argument("-c", '--country', type=str, default="Mexico", help="Specify a single country you would like to generate a prompt for")
    parser.add_argument("-m", "--model", type=str, default="sonar-pro", choices=["gpt-4.1","sonar", "sonar-pro", "sonar-deep-research", "ms_copilot", "mistral", "gemini_2.5_flash"], help="The model that you want to query")


    args = parser.parse_args()

    main(args)   

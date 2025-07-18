import csv
import sys
import logging
import argparse
from propeterra_internship_2025.utils.model_query import QueryModel
from propeterra_internship_2025.data.all_countries import regions, all_countries
from propeterra_internship_2025.utils.prompt_templates import create_real_estate_professional_prompt



logging.basicConfig(level=logging.INFO)


def main(args: argparse.Namespace) -> None:
    '''
    Create prompts for manus to search for real estate professionals in a specific country.
    '''

    system_prompt, user_prompt = create_real_estate_professional_prompt(
                                    country_of_interest=args.country,
                                    system_prompt_num=args.system_prompt_num,
                                    prompt_num=args.prompt_num)
    
    query = QueryModel(model=args.model,  country=args.country, system_prompt=system_prompt,
                       user_prompt=user_prompt, prompt_number=args.prompt_num,
                       system_prompt_number=args.system_prompt_num)
    
    query.initialize_real_estate_professional_search_file()
    
    # query.query_model(real_estate_questions=True)






if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", '--country', type=str, default="Mexico", help="Specify a single country you would like to generate a prompt for")
    parser.add_argument("-m", "--model",   type=str, default="manus", choices=["manus","gpt-4.1","sonar", "sonar-pro", "sonar-deep-research", "ms_copilot", "mistral", "gemini_2.5_flash"], help="The model that you want to query")
    parser.add_argument("-spn", "--system_prompt_num", type=int, default=4, help="The system prompt template that you want to submit to the model. List of all prompts is located in 'prompt templates'")
    parser.add_argument("-pn", "--prompt_num", type=int, default=2, help="The specific question number that you want to query, this is used to select the question from the CSV file")
    args = parser.parse_args()

    main(args)   

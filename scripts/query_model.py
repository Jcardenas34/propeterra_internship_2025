import argparse
from propeterra_internship_2025.data.all_countries import regions
from propeterra_internship_2025.utils.prompt_templates import Prompt

def main(args):
    '''
    Iterate over the countries in the region of interest and submit a querey to the
    LLM (Which can be specified) 
    '''
    # Pre-defined Region of interest, can choose
    # region_of_interest = "Latin America"
    region_of_interest = args.region
    
    for country in regions.get(region_of_interest, "North America")[:2]:
        prompt = Prompt(num_sources=args.n_sources, country_of_interest=country, prompt_num=2).construct_prompt()
        print(prompt, "\n\n")


    # Logic to prompt model


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--region", type=str, default="Latin America", choices=regions.keys(), help="The regions that you want to probe, will loop over all countries in region")
    parser.add_argument("-ns","--n_sources", type=int, default=10, help="The number of links you want to get back from the model")
    parser.add_argument("-pn", "--prompt_num", type=int, default=1, help="The prompt template that you want to submit to the model. List of all prompts is located in 'prompt templates'")
    parser.add_argument("-m", "--model", type=str, default="perplexity", help="The model that you want to query")


    args = parser.parse_args()

    main(args)
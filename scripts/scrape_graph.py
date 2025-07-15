import os
import json
import argparse
from datetime import date
from scrapegraphai.graphs import SmartScraperGraph

from propeterra_internship_2025.utils.api_key_retrieval import RetrieveApiKey



def write_to_file(model:str, country:str , response:str) -> None:
    ''' Writes the response from the model to a text file. And outputs prompt to console'''
    if not os.path.isdir(f"model_output/{country}"):
        os.mkdir(f"model_output/{country}")

    with open(f"model_output/{country}/{model}_{country}_{date.today()}_real_estate_professionals_scrapegraph.txt", 
              "a", encoding="utf8") as file:
        file.write(response)
    print(response)


def main( args ) -> None:
    ''' Will submit a query to an LLM to web scrape according to provided prompt and URL'''

    model_obj = RetrieveApiKey(model=args.model)

    graph_config = {
    "llm": {
        "api_key": model_obj.supported_models[model_obj.model],
        "model": f"openai/{args.model}",
    },
    "verbose": True,
    "headless": False,
    }

    # there are 153 pages
    # https://www.properstar.com/mexico/real-estate-agents
    # https://www.properstar.com/mexico/real-estate-agents?p=XXX


    all_pages = 154
    total_result = ""
    end = 3
    for page_num in range(1, end):
        url = "https://www.properstar.com/mexico/real-estate-agents?p="+str(page_num)
        print(url)
        # Create the SmartScraperGraph instance
        smart_scraper_graph = SmartScraperGraph(
            prompt="The page I have given you should contain 10 real estate professionals with links to their webpage. Please navigate to their page and gather their name, email, phone number, website, 'about me', social media links, affiliated agency, position at the agency, and any other information available for the real estate professionals on this site. Do not retrieve their listings. The JSON file you produce should have entries with all of the same keys, if a key is not available, fill it with NAN.",
            source=url,
            config=graph_config
        )

        # Run the pipeline
        result = smart_scraper_graph.run()
        total_result += json.dumps(result, indent=4)+"\n"

    write_to_file(model=args.model, country=args.country, response=total_result)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", '--country', type=str, default="Mexico", help="Specify a single country you would like to generate a prompt for")
    parser.add_argument("-m", "--model",   type=str, default="gpt-4.1", choices=["manus","gpt-4.1","sonar", "sonar-pro", "sonar-deep-research", "ms_copilot", "mistral", "gemini_2.5_flash"], help="The model that you want to query")
    args = parser.parse_args()

    main(args)   
import csv
import sys
import logging
import argparse
from propeterra_internship_2025.data.all_countries import regions, all_countries
from propeterra_internship_2025.utils.prompt_templates import create_real_estate_question_prompt
from propeterra_internship_2025.utils.model_query import QueryModel



logging.basicConfig(level=logging.INFO)


def main(args: argparse.Namespace) -> None:
    '''
    Iterate over the 100 or 1000 questions about the region of interest and submit a query to the
    LLM (Which can be specified) 
    '''




    file_path = args.infile  # Replace with the path to your CSV file
    
    
    
    # Extracting the 100_questions or 1000_questions from the file name
    if "1000_questions" in file_path:
        file_type = "_of_1000_questions"
    elif "100_questions" in file_path:
        file_type = "_of_100_questions"
    else:
        raise ValueError("The file name must contain either '100_questions' or '1000_questions' to determine the type of questions.")


    with open(file_path, 'r', newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)


        # Select only 1 question specified by the user to submit to the model
        if args.question_num != -1:
            query_limit = 1.0
            reader = [row for idx, row in enumerate(reader) if idx == args.question_num - 1]
            print(f"Querying question number {args.question_num} from the file.")
            print(f"[{args.question_num}] {reader[0][0]}")
        else:
            print(f"Querying all questions from the file: {file_path}")



        for idx, row in enumerate(reader):

            # Changing the prompt index to match the question number that will be printed on the output file
            if args.question_num != -1:
                prompt_index = args.question_num
            else:
                prompt_index = idx + 1

            system_prompt, user_prompt = create_real_estate_question_prompt(
                                            country_of_interest=args.country,
                                            system_prompt_num=args.system_prompt_num,
                                            user_prompt=row[0]
                                            )
            
            query = QueryModel(args.model,  args.country, system_prompt,
                               user_prompt, prompt_index, args.system_prompt_num,
                               outfile_comment=file_type)
            
            print(query.system_prompt+"\n")
            print(query.user_prompt+"\n")
            
            # Ensuring that all prompts have had their respective [country] specific data filled
            # print(f"[{idx+1}] {query.user_prompt}")
            if "[" in query.user_prompt:
                print(f"[{prompt_index}] {query.user_prompt}")
                sys.exit(f"Error: The user prompt contains a placeholder for the country name. Please ensure that the prompt is correctly formatted before submitting to the model.")

            query.initialize_real_estate_questions_file()
            query.query_model_langchain(real_estate_questions=True)


        # print(f"country specific: {100*counter/query_limit}")





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile",  type=str, default="data/2025_INTERNSHIP_ORIENTATION-100_questions.csv", help="The regions that you want to probe, will loop over all countries in region")
    parser.add_argument("-c", '--country', type=str, default="Mexico", help="Specify a single country you would like to generate a prompt for")
    parser.add_argument("-m", "--model",   type=str, default="gpt-4.1", choices=["gpt-4.1","sonar", "sonar-pro", "sonar-deep-research", "ms_copilot", "mistral", "gemini-2.5-flash","gemini-2.5-pro"], help="The model that you want to query")
    parser.add_argument("-spn", "--system_prompt_num", type=int, default=3, help="The system prompt template that you want to submit to the model. List of all prompts is located in 'prompt templates'")
    parser.add_argument("-qn", "--question_num", type=int, default=-1, help="The specific question number that you want to query, this is used to select the question from the CSV file")
    args = parser.parse_args()

    main(args)   

import argparse
from openai import OpenAI
from propeterra_internship_2025.utils.helpers import timing_function

@timing_function
def main(args):
    client = OpenAI()

    # input = args.input
    # input = "What are t"
    response = client.responses.create(
        model=args.model,
        input=args.input,
        # tools=[{"type": "web_search_preview"}],
    )

    print(response.output_text)


if __name__ == "__main__":
    # This block is executed when the script is run directly
    print("OpenAI query script executed.")
    parser = argparse.ArgumentParser(description='Model selection and query')
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo", choices=['gpt-3.5',"gpt-4o"])
    parser.add_argument('-i', "--input",type=str, required=True)

    args = parser.parse_args()

    main(args)

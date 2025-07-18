import json
import requests
import argparse
import logging
import sys



def setup_logger(country):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # File handler
    fh = logging.FileHandler(f"{country}_linvalid_link.log")
    fh.setLevel(logging.INFO)

    # Console handler (optional)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def extract_first_json_object(text):
    """
    Extracts the first top-level { ... } JSON block.
    Uses a simple brace counter.
    """
    brace_stack = []
    start_idx = None

    for idx, char in enumerate(text):
        if char == '{':
            if not brace_stack:
                start_idx = idx
            brace_stack.append('{')
        elif char == '}':
            if brace_stack:
                brace_stack.pop()
                if not brace_stack:
                    end_idx = idx + 1
                    return text[start_idx:end_idx]

    return None  # No valid JSON block found

def check_link(link: str) -> tuple[bool| None, int]:
    """
    Check if a link returns 404 or any other fail type.
    returns: Bool
        True if link is broken and matches any of the failure codes
        False if link is valid
        None if link could not be checked
    """
    fail_types = [204, 400, 401, 404, 405, 408, 410, 429, 502, 503, 504]
    try:
        response = requests.head(link, timeout=5)
        # print(response.status_code)
        if response.status_code in fail_types:
            return True, response.status_code
        else:
            return False, response.status_code
    # except requests.RequestException as e:
    except requests.RequestException:
        # print(f"Error checking link {link}: {e}")
        return None, -1

def scrapeable_link(link:str) -> tuple[bool | None, int]:
    """
    Checks web pages robots.txt for indicators that it does not want to be scraped.
    If 'Disallow: / ' is found, it returns False (Not scrape-able).

    returns: Bool
        True is can be scraped
        False if it cannot be scraped
        None if robots.txt could not be checked
    """

    root_link = link.split('/')[0] + '//' + link.split('/')[2] + '/robots.txt'
    print(f"Checking robots.txt for {root_link}")

    disallow_strings = ["Disallow: / ", "Disallow:/ "]

    try:
        response = requests.get(root_link)
        # print(response.text)
        if response.text in disallow_strings:
            # print(f"Robots.txt disallows scraping for {root_link}")
            return False, -100
        else:
            # print(f"Robots.txt allows scraping for {root_link}")
            return True, 200
        
    except requests.RequestException as e:
        print(f"Error checking link {root_link}: {e}")
        return None, -1
    

def process_file(filename, logger, valid_link_tracker):
    """
    Process a single file and return valid entries + notes.
    """
    with open(filename, 'r', encoding="utf8") as f:
        text = f.read()
        # ensuring that no other json dictionaries in the prompt are read
        text = text[text.find("AI Returned Links:"):]

    json_block = extract_first_json_object(text)

    if not json_block:
        logger.warning(f"[WARN] No JSON block found in '{filename}'")
        return [], [], {}


    try:
        data = json.loads(json_block)
        # print(data)
    except json.JSONDecodeError as e:
        logger.error(f"[ERR] JSON decode error in '{filename}': {e}")
        return [], [], {}

    data_sources = data.get("data_sources", [])
    notes = data.get('notes', {})

    logger.info(f"\n📂 Processing '{filename}' — found {len(data_sources)} sources.")

    valid_entries = []
    # saving invlid links because they are often not entirely invalid, could lead to good sources
    invalid_entries = []

    non_scrapable_links = []


    for idx, item in enumerate(data_sources, 1):
        link = item.get('link')
        if link:
            is_404, code = check_link(link)
            if is_404 is True:
                logger.error(f"[{code}] #{idx}: {link}")
                invalid_entries.append(item)
            elif is_404 is False:
                logger.info(f"[OK ] #{idx}: {link}")
                if link in valid_link_tracker:
                    logger.error(f'Link: {link} is redundant')
                    continue
                else:
                    valid_link_tracker.append(link)
                    valid_entries.append(item)
            else:
                logger.error(f"[ERR] #{idx}: {link} could not be checked.")
                invalid_entries.append(item)
        else:
            logger.warning(f"[WARN] #{idx}: No 'link' field found.")

    logger.info(f"✅ Valid entries in '{filename}': {len(valid_entries)}/{len(data_sources)}")
    return valid_entries, invalid_entries, notes

def main(args):
    # 🔑 List of files to process — adjust as needed!
    input_files = args.input 

    logger = setup_logger(args.country)

    all_valid_entries = []
    all_invalid_entries = []
    valid_link_tracker = []
    notes = {}

    for file in input_files:
        valid_entries, invalid_entries, file_notes = process_file(file, logger, valid_link_tracker)
        all_valid_entries.extend(valid_entries)
        all_invalid_entries.extend(invalid_entries)

        # Keep the notes from the first file as example
        if not notes and file_notes:
            notes = file_notes

    logger.info(f"\n🎉 Total valid entries: {len(all_valid_entries)}/{len(all_valid_entries+all_invalid_entries)}")

    output = {
        "data_sources": all_valid_entries,
        "notes": notes
    }
    dead_links = {
        "data_sources": all_invalid_entries
    }


    with open(f'{args.country}_links.json', 'w') as out_file:
        json.dump(output, out_file, indent=2, ensure_ascii=False)

    with open(f'{args.country}_invalid_links.json', 'w') as out_file:
        json.dump(dead_links, out_file, indent=2, ensure_ascii=False)


    logger.info(f"\n✅ Saved combined valid links to '{args.country}_links.json'.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="country", type=str)
    parser.add_argument(dest="input", nargs="+")
    args = parser.parse_args()
    main(args)
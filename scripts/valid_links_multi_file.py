import json
import requests
import argparse

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

def check_link(link):
    """
    Check if a link returns 404.
    """
    try:
        response = requests.head(link, timeout=5)
        if response.status_code == 404:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error checking link {link}: {e}")
        return None

def process_file(filename):
    """
    Process a single file and return valid entries + notes.
    """
    with open(filename, 'r') as f:
        text = f.read()
        # ensuring that no other json dictionaries in the prompt are read
        text = text[text.find("AI Returned Links:"):]

    json_block = extract_first_json_object(text)

    if not json_block:
        print(f"[WARN] No JSON block found in '{filename}'")
        return [], [], {}


    try:
        data = json.loads(json_block)
        # print(data)
    except json.JSONDecodeError as e:
        print(f"[ERR] JSON decode error in '{filename}': {e}")
        return [], [], {}

    data_sources = data.get("data_sources", [])
    notes = data.get('notes', {})

    print(f"\n📂 Processing '{filename}' — found {len(data_sources)} sources.")

    valid_entries = []
    # saving invlid links because they are often not entirely invalid, could lead to good sources
    invalid_entries = []

    for idx, item in enumerate(data_sources, 1):
        link = item.get('link')
        if link:
            is_404 = check_link(link)
            if is_404 is True:
                print(f"[404] #{idx}: {link}")
                invalid_entries.append(item)
            elif is_404 is False:
                print(f"[OK ] #{idx}: {link}")
                valid_entries.append(item)
            else:
                print(f"[ERR] #{idx}: {link} could not be checked.")
                invalid_entries.append(item)
        else:
            print(f"[WARN] #{idx}: No 'link' field found.")

    print(f"✅ Valid entries in '{filename}': {len(valid_entries)}/{len(data_sources)}")
    return valid_entries, invalid_entries, notes

def main(args):
    # 🔑 List of files to process — adjust as needed!
    input_files = args.input 

    all_valid_entries = []
    all_invalid_entries = []
    notes = {}

    for file in input_files:
        valid_entries, invalid_entries, file_notes = process_file(file)
        all_valid_entries.extend(valid_entries)
        all_invalid_entries.extend(invalid_entries)

        # Keep the notes from the first file as example
        if not notes and file_notes:
            notes = file_notes

    print(f"\n🎉 Total valid entries: {len(all_valid_entries)}")

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


    print(f"\n✅ Saved combined valid links to '{args.country}_links.json'.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", dest="country", type=str)
    parser.add_argument(dest="input", nargs="+")
    args = parser.parse_args()
    main(args)
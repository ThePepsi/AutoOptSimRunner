import re

def read_last_block(file_path):
    
    # Read the entire file
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content using a regular expression for lines with many '#'
    # This regex looks for lines that are composed mostly of '#'
    blocks = re.split(r'\n#+\n', content)

    # Return the last block (ignoring empty blocks at the end)
    for block in reversed(blocks):
        if block.strip():  # Check if the block is not just empty space
            return block

    # Return an empty string if no blocks are found
    return ""


def find_block_with_text(text, search_text):
    # Split the content using a regular expression for lines with many '-'
    blocks = re.split(r'\n-+\n', text)

    # Search for the block containing the specified text
    for block in blocks:
        if search_text in block:
            return block

    # Return an empty string if the text is not found in any block
    return ""


def extract_scenario_data(text):
    # Regular expression to match the pattern and capture variable names and values
    pattern = r"\*\.node\[\*\]\.scenario\.([a-zA-Z0-9_]+)\s*:\s*(.+)"
    matches = re.findall(pattern, text)

    # Creating a dictionary from the matches
    var_dict = {var: value for var, value in matches}

    return var_dict


# Usage
file_path = 'C:\\Users\\timos\\Documents\\Work\\11_WiSe2324\\01_BA\\04_Git\\AutoOptSimRunner\\text2value\\out.txt'
last_block = read_last_block(file_path)
block_with_text = find_block_with_text(last_block,"1. Result")
scenario_data = extract_scenario_data(block_with_text)
print(scenario_data)
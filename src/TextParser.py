import re

class TextParser:
        
    def parse_data(self, file_path):
        last_block = self._read_last_block(file_path)
        right_block = self._find_right_result(last_block, "1. Result")
        return self._extract_scenario_data(right_block)

    def _read_last_block(self, file_path):
        
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


    def _find_right_result(self, text, search_text):
        # Split the content using a regular expression for lines with many '-'
        blocks = re.split(r'\n-+\n', text)

        # Search for the block containing the specified text
        for block in blocks:
            if search_text in block:
                return block

        # Return an empty string if the text is not found in any block
        return ""


    def _extract_scenario_data(self, text):
        # Regular expression to match the pattern and capture variable names and values
        pattern = r"\*\.node\[\*\]\.scenario\.([a-zA-Z0-9_]+)\s*:\s*(.+)"
        matches = re.findall(pattern, text)

        # Creating a dictionary from the matches
        var_dict = {var: value for var, value in matches}

        return var_dict
    

import re

class TextParser:
        
    def parse_data(self, file_path):
        last_block = self._read_last_block(file_path)
        right_block = self._find_right_result(last_block, "1. Result")
        scenario_data = self._extract_scenario_data(right_block)

        penultimate_block = self._read_penultimate_block(file_path)
        sim_data = self._extract_sim_data(penultimate_block)
        scenario_data.update(sim_data)

        return scenario_data

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
    
    def _extract_sim_data(self, block):
        for line in block.split('\n'):
        # Data Stuff
            if "Iterations:" in line:
                _Iterations = int(line.split(":\t")[1])
            if "Iterations without improvement:" in line:
                _Iterationswithoutimprovement = int(line.split(":\t")[1])
            if "Evaluations:" in line:
                _Evaluations = int(line.split(":\t")[1])
            if "Value:" in line:
                _Value = float(line.split(" ")[1])
        
        return {
            'Iterations': _Iterations,
            'Evaluations': _Evaluations,
            'Value': _Value
        }
        
    def _read_penultimate_block(self, file_path):
        # Read the entire file
        with open(file_path, 'r') as file:
            content = file.read()

        # Split the content using a regular expression for lines with many '#'
        blocks = re.split(r'\n#+\n', content)

        # Initialize a variable to keep track of the last non-empty block found
        last_non_empty_block = None

        # Iterate through the blocks in reverse order
        for block in reversed(blocks):
            if block.strip():  # Check if the block is not just empty space
                if last_non_empty_block is not None:
                    # If we've already found a non-empty block, return the current one as it is the penultimate block
                    return block
                # Update the last non-empty block found
                last_non_empty_block = block

        # Return an empty string if no blocks are found or there is only one non-empty block
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
    

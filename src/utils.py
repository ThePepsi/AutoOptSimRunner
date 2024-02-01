import itertools
from src.ControllerType import ControllerType

class utils:
    def find_new_combination(input_enVar_json, checkdatabase):
        # Kinda Override range() to use float
        def float_range(start, stop, step):
            while start <= stop:
                yield round(start, 10)  # Round to prevent floating-point arithmetic issues
                start += step

        # Generate all possible combinations
        def generate_combinations(range_info):
            return [i for i in float_range(range_info["min"], range_info["max"] + 1, int((range_info["max"] - range_info["min"]) / range_info["step"]))]

        leaderSpeed_values = generate_combinations(input_enVar_json["leaderSpeed"])
        errorrate_values = generate_combinations(input_enVar_json["frameErrorRate"])
        controller_values = input_enVar_json["controller"]

        all_combinations = itertools.product(leaderSpeed_values, errorrate_values, controller_values)

        # Get already used combinations
        used_combinations = checkdatabase()

        # Find a new combination
        for combination in all_combinations:
            if combination not in used_combinations:
                return {"controller": combination [2], "leaderSpeed": combination[0], "frameErrorRate": combination[1]}

        return None # In case all combinations are used
    
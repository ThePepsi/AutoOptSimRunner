used_values = [(10, 0.0), (20, 0.1)]
def check(value_pair):
    # Dummy implementation of check method
    # Replace this with your actual check logic
    # Return True if the pair has been used, False otherwise
    #used_values = [(10, 0.0), (20, 0.1)]  # Example of used pairs
    return value_pair in used_values



def generate_value_pair(steps):
    # Test the function
    steps = {
        "leaderspeed": {
            "min": 10,
            "max": 200,
            "step": 10
        },
        "frameErrorRate": {
            "min": 0.0,
            "max": 1.0,
            "step": 0.1
        }
    }
    # Kinda Override range() to use float
    def float_range(start, stop, step):
        while start <= stop:
            yield round(start, 10)  # Round to prevent floating-point arithmetic issues
            start += step

    params1 = steps["leaderspeed"]
    params2 = steps["frameErrorRate"]

    min1, max1, step1 = params1["min"], params1["max"], params1["step"]
    min2, max2, step2 = params2["min"], params2["max"], params2["step"]

    for value1 in float_range(min1, max1, step1):
        for value2 in float_range(min2, max2, step2):
            value_pair = (value1, value2)
            if not check(value_pair):
                return value_pair

    return None  # Return None if no unused pair is found


for x in range(0,100):
    value_pair = generate_value_pair(steps)
    used_values.append(value_pair)
    print(value_pair)
import os
import subprocess

try:
    command = f'(cd && cd src/simopticon/build/ && ./simopticon ../config/simopticon.json)'
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)

    with open('output.txt','w') as file:
        file.write(result.stdout)
except FileNotFoundError:
    print("FileError")
except Exception as e:
    print(f"Fail: {str(e)}")
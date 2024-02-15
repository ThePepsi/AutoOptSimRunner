import os
file_path = 'src/veins/'
if os.path.exists(file_path):
    #os.remove(file_path)
    print("yes")
else:
    print("no")

f = []
for entry in os.scandir('/home/plexe/src'):
    print(entry)
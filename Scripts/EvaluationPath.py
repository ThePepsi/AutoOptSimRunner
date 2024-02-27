
file_path = input ("FileName:")
with open(file_path, 'r') as file:
    content = file.read()

blocks = content.split('######################################################################')
blocks = blocks[1:-1]
r_blocks = []
for b in blocks:
    if "Value: inf" in b:
        r_blocks.append(b)
for b in r_blocks:
    blocks.remove(b)

class Data:
    def __init__(self, Iterations, Iterationswithoutimprovement, Evaluations, Value):
        self.Iterations = Iterations
        self.Iterationswithoutimprovement = Iterationswithoutimprovement
        self.Evaluations = Evaluations
        self.Value = Value

    def combinedStringData(self):
        return "; ".join([str(self.Iterations), str(self.Iterationswithoutimprovement), str(self.Evaluations), str(self.Value)])
    
    def combinedStringHead(self):
        return "; ".join(["Iterations", "Iterationswithoutimprovement", "Evaluations", "Value"])

class Controller:
    pass

class CACC(Controller):
    def __init__(self, caccC1, caccOmegaN, caccXi):
        self.caccC1 = caccC1
        self.caccOmegaN = caccOmegaN
        self.caccXi = caccXi
    
    def combinedStringData(self):
        return "; ".join([str(self.caccC1), str(self.caccOmegaN), str(self.caccXi)])
    
    def combinedStringHead(self):
        return "; ".join(["caccC1", "caccOmegaN", "caccXi"])

_donelist = []
    
for block in blocks:

    for line in block.split('\n'):
       # Data Stuff
        if "Iterations:" in line:
            _Iterations = int(line.split(":\t")[1])
        if "Iterations without improvement:" in line:
            _Iterationswithoutimprovement = int(line.split(":\t")[1])
        if "Evaluations:" in line:
            _Evaluations = int(line.split(":\t")[1])
        if "Value:" in line:
            _Value = float(line.split(":\t")[1])

        # CACC Stuff
        if "caccC1" in line:
            _caccC1 = float(line.split(":\t")[1])
        if "caccOmegaN" in line:
            _caccOmegaN = float(line.split(":\t")[1].replace("Hz",""))
        if "caccXi" in line:
            _caccXi = float(line.split(":\t")[1])
        
        # TODO Do more Controller here
            
    if "caccC1" in block and "caccOmegaN" in block and "caccXi" in block:
        _controller = CACC(_caccC1, _caccOmegaN, _caccXi)

    # TODO Do more Controller here
    

    _data = Data(_Iterations,_Iterationswithoutimprovement, _Evaluations, _Value)
            
    _donelist.append((_data, _controller))
      


with open(file_path.replace("txt","csv"), 'w') as file:
    # Printing Part
    head = _donelist[0][0].combinedStringHead() +";"+ _donelist[0][1].combinedStringHead()
    file.write(head+"\n")
    for (__data, __controller) in _donelist:
        date = __data.combinedStringData() + ";" + __controller.combinedStringData()
        file.write(date+"\n")



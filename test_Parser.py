import unittest, json, os
from src.TextParser import TextParser

class Parser_TestCase(unittest.TestCase):
   

    def setUp(self):
        self.parser = TextParser()
        self.testPath = os.path.join("src", "out.txt")


    # def test_parse_lastBlock(self):
    #     calc_last_block = self.parser._read_last_block(self.testPath)
    #     print(calc_last_block)
    #     self.assertEqual(last_block, calc_last_block)  

    def test_parse_rightResult(self):
        calc_rightResult = self.parser._find_right_result(last_block,"1. Result")
        self.assertEqual(block_with_text, calc_rightResult)

    def test_parse_scenarioData(self):
        calc_scenarioData = self.parser._extract_scenario_data(last_block)
        self.assertEqual(scenario_data, calc_scenarioData)    

    def test_parse_all(self):
        self.assertEqual(scenario_data, self.parser.parse_data(self.testPath))  


last_block = '''10. Result
*.node[*].scenario.caccC1:	1
*.node[*].scenario.caccOmegaN:	3.36667Hz
*.node[*].scenario.caccXi:	2.33333
Value: 0.000382468
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/7"
----------------------------------------------------------------------
9. Result
*.node[*].scenario.caccC1:	0.333333
*.node[*].scenario.caccOmegaN:	3.36667Hz
*.node[*].scenario.caccXi:	5
Value: 0.000381163
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/8"
----------------------------------------------------------------------
8. Result
*.node[*].scenario.caccC1:	0.444444
*.node[*].scenario.caccOmegaN:	6.68333Hz
*.node[*].scenario.caccXi:	3.66667
Value: 0.000320079
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/19"
----------------------------------------------------------------------
7. Result
*.node[*].scenario.caccC1:	0.555556
*.node[*].scenario.caccOmegaN:	3.36667Hz
*.node[*].scenario.caccXi:	5
Value: 0.000305907
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/20"
----------------------------------------------------------------------
6. Result
*.node[*].scenario.caccC1:	0.777778
*.node[*].scenario.caccOmegaN:	3.36667Hz
*.node[*].scenario.caccXi:	5
Value: 0.000279087
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/18"
----------------------------------------------------------------------
5. Result
*.node[*].scenario.caccC1:	1
*.node[*].scenario.caccOmegaN:	3.36667Hz
*.node[*].scenario.caccXi:	5
Value: 0.000277455
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/5"
----------------------------------------------------------------------
4. Result
*.node[*].scenario.caccC1:	0.666667
*.node[*].scenario.caccOmegaN:	6.68333Hz
*.node[*].scenario.caccXi:	3.66667
Value: 0.000271987
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/12"
----------------------------------------------------------------------
3. Result
*.node[*].scenario.caccC1:	0.888889
*.node[*].scenario.caccOmegaN:	6.68333Hz
*.node[*].scenario.caccXi:	3.66667
Value: 0.000252602
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/17"
----------------------------------------------------------------------
2. Result
*.node[*].scenario.caccC1:	0.777778
*.node[*].scenario.caccOmegaN:	10Hz
*.node[*].scenario.caccXi:	5
Value: 0.000213233
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/16"
----------------------------------------------------------------------
1. Result
*.node[*].scenario.caccC1:	1
*.node[*].scenario.caccOmegaN:	10Hz
*.node[*].scenario.caccXi:	5
Value: 0.000184226
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/1"
----------------------------------------------------------------------
1.	0.000184226
2.	0.000213233
3.	0.000252602
4.	0.000271987
5.	0.000277455
6.	0.000279087
7.	0.000305907
8.	0.000320079
9.	0.000381163
10.	0.000382468'''
block_with_text = '''1. Result
*.node[*].scenario.caccC1:	1
*.node[*].scenario.caccOmegaN:	10Hz
*.node[*].scenario.caccXi:	5
Value: 0.000184226
Path to result files: "/home/plexe/src/plexe/examples/platooning/optResults/1"'''
scenario_data = {'caccC1': '1', 'caccOmegaN': '10Hz', 'caccXi': '5'}
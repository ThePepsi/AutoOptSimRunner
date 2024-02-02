import unittest
from src.DB_CLI import DB_CLI

class TestCLIApplication_TestCase(unittest.TestCase):

    def test_generate_combinations_basic(self):
        app = DB_CLI()
        app.leaderSpeed = [10, 20]
        app.braking = [1, 2]
        app.errorRate = [2]
        expected_combinations = [(10, 1, 2), (10, 2, 2), (20, 1, 2), (20, 2, 2)]
        self.assertEqual(app.generate_combinations(), expected_combinations)

    def test_generate_combinations_empty_lists(self):
        app = DB_CLI()
        # Leere Listen führen zu einem Ergebnis mit einem Tupel von None-Werten, wenn Sie die None-Platzhalter entfernen.
        expected_combinations = [(None, None, None)]
        self.assertEqual(app.generate_combinations(), expected_combinations)

    def test_generate_combinations_one_empty_list(self):
        app = DB_CLI()
        app.leaderSpeed = [10, 20]
        app.braking = []  # Leere Liste
        app.errorRate = [2]
        # Erwarten Sie Kombinationen, die None für 'braking' enthalten, wenn Sie die None-Platzhalter entfernen.
        expected_combinations = [(10, None, 2), (20, None, 2)]
        self.assertEqual(app.generate_combinations(), expected_combinations)

    
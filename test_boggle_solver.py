import unittest
from boggle_solver import Boggle


class TestSuiteAlgScalability(unittest.TestCase):

    def test_normal_case_3x3(self):
        grid = [["A", "B", "C"],
                ["D", "E", "F"],
                ["G", "H", "I"]]

        dictionary = ["abc", "abdhi", "abi", "ef", "cfi", "dea"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]

        expected = ["abc", "abdhi", "cfi", "dea"]
        expected = [x.upper() for x in expected]

        self.assertEqual(sorted(expected), sorted(solution))


class TestSuiteSimpleEdgeCases(unittest.TestCase):

    def test_square_grid_1x1(self):
        grid = [["A"]]
        dictionary = ["a", "b", "c"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]

        expected = []
        self.assertEqual(sorted(expected), sorted(solution))

    def test_empty_grid(self):
        grid = []
        dictionary = ["hello", "there", "general", "kenobi"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]

        expected = []
        self.assertEqual(sorted(expected), sorted(solution))

    def test_no_matches(self):
        grid = [["A","B"],["C","D"]]
        dictionary = ["xyz", "zzz"]
        mygame = Boggle(grid, dictionary)
        self.assertEqual([], mygame.getSolution())

    def test_single_match(self):
        grid = [["C","A","T"]]
        dictionary = ["cat","dog"]
        mygame = Boggle(grid, dictionary)
        self.assertIn("cat", [x.lower() for x in mygame.getSolution()])


class TestSuiteQuAndSt(unittest.TestCase):

    def test_qu_case(self):
        grid = [["Qu","A","R","T"]]
        dictionary = ["quart", "qua"]
        mygame = Boggle(grid, dictionary)
        solution = [x.lower() for x in mygame.getSolution()]

        self.assertIn("qua", solution)

    def test_st_case(self):
        grid = [["S","T","A","R"]]
        dictionary = ["star", "tar"]
        mygame = Boggle(grid, dictionary)
        solution = [x.lower() for x in mygame.getSolution()]

        self.assertIn("star", solution)


class TestSuiteCoverage(unittest.TestCase):

    def test_duplicate_dictionary(self):
        grid = [["C","A","T"]]
        dictionary = ["cat", "cat"]
        mygame = Boggle(grid, dictionary)
        result = mygame.getSolution()

        self.assertEqual(len(result), len(set(result)))

    def test_case_insensitive(self):
        grid = [["C","A","T"]]
        dictionary = ["CAT"]
        mygame = Boggle(grid, dictionary)

        self.assertIn("CAT", mygame.getSolution())

    def test_large_dictionary(self):
        grid = [["C","A","T"]]
        dictionary = ["cat"] * 100
        mygame = Boggle(grid, dictionary)

        self.assertTrue(len(mygame.getSolution()) >= 1)

    def test_returns_list(self):
        grid = [["A","B"],["C","D"]]
        dictionary = ["ab"]
        mygame = Boggle(grid, dictionary)

        self.assertIsInstance(mygame.getSolution(), list)


if __name__ == "__main__":
    unittest.main()

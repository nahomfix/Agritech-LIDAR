import unittest

import pandas as pd
from scripts.load_data import LoadData


class TestLoadData(unittest.TestCase):
    def setUp(self) -> None:
        try:
            data = pd.read_csv("../data/IL_BooneCo_2007.csv")
            self.dataframe = data
        except IOError:
            print("could not open csv file")

    def test_fetch_data(self):
        loaded_data = LoadData(
            [-9619500, 5187800],
            [-9618900, 5188500],
            "IL_BooneCo_2007",
        )

        data_dict = loaded_data.fetch_data()

        self.assertEqual(data_dict, {"2007": self.dataframe})


if __name__ == "__main__":
    unittest.main()

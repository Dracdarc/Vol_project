import pandas as pd
from os import path
from matplotlib import pyplot as plt


DATA_DIR: str = path.normpath(
    path.split(path.realpath(__file__))[0] + "/../data"
)
INDEX: [str] = ["DJX", "NDX", "SPX"]
YEARS: "Dict str -> [int]" = dict()
YEARS["DJX"] = [2001, 2008, 2018]
YEARS["NDX"] = [2001, 2008, 2018]
YEARS["SPX"] = [2001, 2008, 2015]


def Data_visualization(index: str) -> None:
    data: "pd.DataFrame"
    n_years: int = len(YEARS[index])
    fig, axes = plt.subplots(nrows=n_years, ncols=1)
    for i in range(n_years):
        data = pd.read_csv(
            DATA_DIR + "/OptionMetric_{}_{}_DATA.csv".format(
                YEARS[index][i], index
            )
        )
        print(data)


if __name__ == "__main__":
    index: str = INDEX[
        int(input("What index ? (0: DJX, 1: NDX, 2: SPX)\n>> "))
    ]
    Data_visualization(index)

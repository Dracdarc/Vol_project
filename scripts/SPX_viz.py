import pandas as pd
from os import path
from matplotlib import pyplot as plt


DATA_DIR: str = path.normpath(
    path.split(path.realpath(__file__))[0] + "/../unzipped_data"
)
YEARS: [int] = [2001, 2008, 2015, 2018]
N_YEARS: int = len(YEARS)


def SPX_visualization() -> None:
    data: "pd.DataFrame"
    fig, axes = plt.subplots(nrows=4, ncols=1)
    for i in range(N_YEARS):
        data = pd.read_csv(
            DATA_DIR + "/CRSP_{}_SPX.csv".format(YEARS[i])
        )
        data.set_index('caldt', drop=True, inplace=True)
        data.plot(ax=axes[i])
    plt.show()


if __name__ == "__main__":
    SPX_visualization()

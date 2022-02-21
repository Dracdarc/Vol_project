import pandas as pd
from os import path


DATA_DIR: str = path.normpath(
    path.split(path.realpath(__file__))[0] + "/../data"
)
YEARS: [int] = [2001, 2008, 2015, 2018]


def yyyymmdd_to_y(date_wrong_format: int) -> float:
    date_str: str = str(date_wrong_format)
    years: float = float(date_str[:4])
    months: float = float(date_str[4:6])/12.
    days: float = float(date_str[6:])/365.25
    return years + months + days


def get_data(
    year: int
) -> [[float]]:
    """
    return a list containing the time list then the SPX prices list
    """
    data: [[float]] = [[0.], [0.]]

    if year in YEARS:
        data_pd: "pd.DataFrame" = pd.read_csv(
            DATA_DIR + "/CRSP_{}_SPX.csv".format(year)
        )
        data[0] = [
            yyyymmdd_to_y(date) for date in data_pd['caldt'].tolist()
        ]
        data[1] = data_pd['spindx'].values.tolist()

    return data

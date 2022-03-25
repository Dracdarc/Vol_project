import pandas as pd


def get_option_data(
    year: int,
    data_folder_path: str,
    want_call: bool = True
) -> pd.DataFrame:
    option_data: pd.DataFrame = pd.read_csv(
        data_folder_path + "/OptionMetric_{}_SPX_DATA.csv".format_map(year)
    )

    option_data = option_data[option_data["exercise_style"] == 'E']
    option_data = option_data[option_data["exdate"] < (year+1)*10000]
    option_data = option_data[
        option_data["cp_flag"] == ("C" if want_call else "P")
    ]

    for column in ["Date", "exdate", "last_date"]:
        option_data[column] = pd.to_datetime(
            option_data[column], format="%Y%m%d"
        )

    option_data["option_price"] = .5 * (
        option_data["best_bid"] + option_data["best_offer"]
    )
    option_data["strike_price"] /= 1000

    return option_data

from functions.math_utility import ln, avg

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from sklearn import mixture

dt: float = 1./365.25


INDEX_NAME: "{str: str}" = {
    "SPX": "^GSPC",
    "DJX": "^DXL",
    "NDX": "^NDX"
}


def get_param(time: [float], asset_values: [float]) -> (float):
    """
    Return a tuple with the drift then the realized volatility.
    """
    n_step: int = len(time) - 1
    dt: [float] = [time[i+1] - time[i] for i in range(n_step)]
    dt_avg: float = avg(dt)
    log_values: [float] = [ln(value) for value in asset_values]
    d_log_values: [float] = [
        log_values[i+1] - log_values[i] for i in range(n_step)
    ]
    alpha: float = avg(d_log_values)
    center_2_dlog: [float] = [(value - alpha)**2 for value in d_log_values]
    sigma_2: float = avg(center_2_dlog) * (n_step-1)/(n_step-2) / dt_avg
    return (alpha/dt_avg + .5*sigma_2, sigma_2**.5)


def get_asset_data(name: str, year: int, past_period: int) -> pd.DataFrame:
    """
    Return asset values for 'past_period' year til 'year'.
    """
    asset_data: pd.DataFrame
    asset_data = yf.Ticker(INDEX_NAME[name]).history(period="max")[["Open"]]
    asset_data = asset_data[str(year - past_period): str(year-1)]
    asset_data = asset_data.rename(columns={'Open': 'asset_price'})
    return asset_data


def get_asset_param(name: str, year: int, past_period: int) -> (float):
    """
    Return asset param calculated on 'past_period' years before 'year'.
    """
    asset_data: pd.DataFrame = get_asset_data(name, year, past_period)
    if len(asset_data):
        time_line: [float] = [0.]
        for _ in range(len(asset_data) - 1):
            time_line.append(time_line[-1] + dt)
        return get_param(time_line, list(asset_data['asset_price']))
    else:
        return (-1, -1)


def get_realized_volatility_list(
    name: str, date_series: "pd.series", days_retro: int = 25
) -> [float]:
    realized_volatility: [float] = []
    asset_data: pd.DataFrame = get_asset_data(
        name, date_series.iloc[-1].year + 1, past_period=2
    ).reset_index()
    index: int = asset_data.index[
        asset_data["Date"] == date_series[0]
    ].to_list()[0]
    local_info: pd.DataFrame
    time_line: [float] = [i*dt for i in range(days_retro)]
    for i in range(len(date_series)):
        local_info = asset_data[(index-days_retro):index]
        realized_volatility.append(
            get_param(
                time_line,
                local_info["asset_price"].to_list()
            )[1]
        )
        index += 1
    return realized_volatility


def get_market_cycle(
    name: str, year: int, past_period: int, n_cluster: int = 3
) -> "pd.DataFrame":
    asset_data: pd.DataFrame = get_asset_data(
        name, year + 1, past_period + 1
    ).reset_index()
    asset_data["dlog_price"] = \
        asset_data["asset_price"] / asset_data["asset_price"].shift(1) - 1
    asset_data["sigma_srdt"] = \
        asset_data["dlog_price"].rolling(25).std()
    asset_data = asset_data.drop(
        asset_data[
            asset_data["Date"].dt.year == asset_data["Date"].iloc[0].year
        ].index
    )
    asset_data["cycle"] = mixture.GaussianMixture(
        n_components=n_cluster, covariance_type="full"
    ).fit(asset_data[["dlog_price", "sigma_srdt"]]).predict(
        asset_data[["dlog_price", "sigma_srdt"]]
    )
    return asset_data.drop(
        columns=["dlog_price", "sigma_srdt"]
    ).reset_index(drop=True)


def display_asset(name: str, year: int, past_period: int) -> None:
    """
    Show the asset prices between year-past_period and year.
    """
    get_asset_data(name, year, past_period)["asset_price"].plot()
    plt.show()

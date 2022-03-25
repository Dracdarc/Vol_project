from functions.math_utility import ln, avg

import pandas as pd
import yfinance as yf

dt: float = 1./365.25


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


def get_SPX_data(year: int, past_period: int) -> pd.DataFrame:
    """
    Return asset values for 'past_period' year til 'year'.
    """
    asset_data: pd.DataFrame
    asset_data = yf.Ticker("^GSPC").history(period="max")[["Open"]]
    asset_data = asset_data[str(year - 1 - past_period): str(year - 1)]
    asset_data = asset_data.rename(columns={'Open': 'asset_price'})
    return asset_data


def get_SPX_param(year: int, past_period: int) -> (float):
    """
    Return SPX param calculated on 'past_period' years before 'year'.
    """
    spx_data: pd.DataFrame = get_SPX_data(year, past_period)
    if len(spx_data):
        time_line: [float] = [0.]
        for _ in range(len(spx_data) - 1):
            time_line.append(time_line[-1] + dt)
        return get_param(time_line, list(spx_data['asset_price']))
    else:
        return (-1, -1)


def display_SPX(year: int, past_period: int) -> None:
    """
    Show SPX between year-1-past_period and year.
    """
    get_SPX_data(year, past_period)["asset_price"].plot()
    plt.show()

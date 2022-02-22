import numpy as np
from matplotlib import pyplot as plt
from functions.math_utility import normal_df, get_delta, exp


plt.style.use('ggplot')


def actual_strategy_pnl(
    asset_prices: [float],
    time: [float],
    actual_vol: float,
    implied_vol: float,
    strike: float,
    interest: float,
    dividend: float,
    drift: float,
    op_type: str
) -> [float]:
    n_steps_time: int = len(asset_prices)-1
    dt: [float] = [time[i+1]-time[i] for i in range(n_steps_time)]
    coef_1: float = .5*(actual_vol**2 - implied_vol**2)*strike/implied_vol
    coef_2: float = drift - interest + dividend

    dpnl: [float] = [0. for _ in range(n_steps_time)]
    pnl: [float] = [0. for _ in range(n_steps_time + 1)]

    def get_jump(i_t: int) -> float:
        return (
            (asset_prices[i_t-1]-asset_prices[i_t]
             - drift*asset_prices[i_t]*dt[i_t])
            / (actual_vol*asset_prices[i_t])
        )

    d1: float
    d2: float
    delta_a: float
    delta_i: float
    tau: float
    sqrt_tau: float
    exp_rtau: float
    for i_t in range(n_steps_time):
        tau = time[-1] - time[i_t]
        sqrt_tau = tau**.5
        exp_rtau = exp(-interest*tau)
        delta_a = get_delta(
            asset_prices[i_t], actual_vol, tau, strike,
            interest, dividend, op_type
        )[0]
        (delta_i, d1, d2) = get_delta(
            asset_prices[i_t], implied_vol, tau, strike,
            interest, dividend, op_type
        )
        dpnl[i_t] = (
            coef_1*dt[i_t]*exp_rtau*normal_df(d2)/sqrt_tau
            + (coef_2*dt[i_t] + actual_vol*get_jump(i_t))
            * asset_prices[i_t] * (delta_i - delta_a)
        )

    for i in range(n_steps_time):
        pnl[i+1] = exp(interest*dt[i])*pnl[i] + dpnl[i]
    for i in range(n_steps_time):
        pnl[i] *= exp(-interest*time[i])

    return pnl


def actual_pnl_simulation(
    n_simulation: int,
    actual_vol: float,
    implied_vol: float,
    expiry_date: float,
    strike: float,
    interest: float,
    dividend: float,
    drift: float,
    asset_price0: float,
    n_steps_time: int,
    op_type: str
) -> None:
    """
    Full simulation : asset price then P&L
    """

    dt: float = expiry_date/n_steps_time
    t_list: [float] = [i*dt for i in range(n_steps_time)]
    sqrt_dt: float = dt**.5

    asset_prices: [[float]] = [
        [asset_price0 for __ in range(n_steps_time)]
        for _ in range(n_simulation)
    ]
    for sim in range(n_simulation):
        for i in range(n_steps_time-1):
            asset_prices[sim][i+1] = asset_prices[sim][i] \
                * (1 + drift*dt + actual_vol*np.random.normal(0., sqrt_dt))

    pnl: [[float]] = [
        actual_strategy_pnl(
            asset_prices[i], t_list, actual_vol, implied_vol,
            strike, interest, dividend, drift, op_type
        ) for i in range(n_simulation)
    ]

    fig, axs = plt.subplots(2)
    for sim in range(n_simulation):
        axs[0].plot(t_list, asset_prices[sim])
        axs[1].plot(t_list, pnl[sim])
    axs[0].set_title("Underlying price")
    axs[1].set_title("""Profit and Loss""")
    for ax in axs.flat:
        ax.set(xlabel="Time in year", ylabel="Price")
        ax.label_outer()
    plt.show()

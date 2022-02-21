import numpy as np
from matplotlib import pyplot as plt
from functions.math_utility import normal_df, normal_cdf, exp, ln, avg


plt.style.use('ggplot')


def actual_pnl_full_simulation(
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
    coef_1: float = dt*.5*(actual_vol**2 - implied_vol**2)*strike/implied_vol
    coef_2: float = (drift - interest + dividend)*dt

    asset_prices: [float] = [asset_price0]
    for _ in range(n_steps_time-1):
        asset_prices.append(
            asset_prices[-1]
            * (1 + drift*dt + actual_vol*np.random.normal(0., sqrt_dt))
        )

    brownian_jumps: [[float]] = [
        [np.random.normal(0., sqrt_dt) for __ in range(n_steps_time-1)]
        for _ in range(n_simulation)
    ]
    dpnl: [[float]] = [
        [0. for __ in range(n_steps_time-1)]
        for _ in range(n_simulation)
    ]
    pnl: [[float]] = [
        [0. for __ in range(n_steps_time)]
        for _ in range(n_simulation)
    ]

    def delta(
        sigma: float,
        tau: float,
        i_t: int,
        op__type: str = op_type
    ) -> (float):
        alpha: float = sigma * tau**.5
        d1: float = (ln(asset_prices[i_t] / strike)
                     + (interest-dividend+sigma**2/2.)*tau) / alpha
        d2: float = d1 - alpha
        delta_res: float
        if op__type.lower() == "call":
            delta_res = exp(-dividend*tau)*normal_cdf(d1)
        else:
            delta_res = -exp(-dividend*tau)*normal_cdf(-d1)
        return (delta_res, d1, d2)

    d1: float
    d2: float
    delta_a: float
    delta_i: float
    tau: float
    sqrt_tau: float
    exp_rtau: float
    for i_t in range(n_steps_time-1):
        tau = expiry_date - t_list[i_t]
        sqrt_tau = tau**.5
        exp_rtau = exp(-interest*tau)
        delta_a = delta(actual_vol, tau, i_t)[0]
        (delta_i, d1, d2) = delta(implied_vol, tau, i_t)
        for sim in range(n_simulation):
            dpnl[sim][i_t] = (
                coef_1*exp_rtau*normal_df(d2)/sqrt_tau
                + (coef_2 + actual_vol*brownian_jumps[sim][i_t])
                * asset_prices[i_t] * (delta_i - delta_a)
            )

    interest_factor: float = exp(interest*dt)
    for sim in range(n_simulation):
        for i in range(n_steps_time-1):
            pnl[sim][i+1] = interest_factor*pnl[sim][i] + dpnl[sim][i]
        for i in range(1, n_steps_time):
            pnl[sim][i] *= exp(-interest*t_list[i])

    fig, axs = plt.subplots(3)
    axs[0].plot(t_list, asset_prices)
    axs[0].set_title("Underlying price")
    for sim in range(n_simulation):
        axs[1].plot(t_list, pnl[sim])
    axs[1].set_title("""Profit and Loss""")
    axs[2].plot(
        t_list,
        [
            avg([pnl[sim][i] for sim in range(n_simulation)])
            for i in range(n_steps_time)
        ]
    )
    axs[2].set_title("""Average Profit and Loss""")
    for ax in axs.flat:
        ax.set(xlabel="Time in year", ylabel="Price")
        ax.label_outer()
    plt.show()


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
    sqrt_dt: [float] = [dt_**.5 for dt_ in dt]
    coef_1: float = .5*(actual_vol**2 - implied_vol**2)*strike/implied_vol
    coef_2: float = drift - interest + dividend

    brownian_jumps: [float] = [np.random.normal(0, dt05) for dt05 in sqrt_dt]
    dpnl: [float] = [0. for _ in range(n_steps_time)]
    pnl: [float] = [0. for _ in range(n_steps_time + 1)]

    def delta(
        sigma: float,
        tau: float,
        i_t: int,
        op__type: str = op_type
    ) -> (float):
        alpha: float = sigma * tau**.5
        d1: float = (ln(asset_prices[i_t] / strike)
                     + (interest-dividend+sigma**2/2.)*tau) / alpha
        d2: float = d1 - alpha
        delta_res: float
        if op__type.lower() == "call":
            delta_res = exp(-dividend*tau)*normal_cdf(d1)
        else:
            delta_res = -exp(-dividend*tau)*normal_cdf(-d1)
        return (delta_res, d1, d2)

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
        delta_a = delta(actual_vol, tau, i_t)[0]
        (delta_i, d1, d2) = delta(implied_vol, tau, i_t)
        dpnl[i_t] = (
            coef_1*dt[i_t]*exp_rtau*normal_df(d2)/sqrt_tau
            + (coef_2*dt[i_t] + actual_vol*brownian_jumps[i_t])
            * asset_prices[i_t] * (delta_i - delta_a)
        )

    for i in range(n_steps_time):
        pnl[i+1] = exp(interest*dt[i])*pnl[i] + dpnl[i]
    for i in range(n_steps_time):
        pnl[i] *= exp(-interest*time[i])

    return pnl

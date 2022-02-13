import numpy as np
from matplotlib import pyplot as plt
from functions.utility import normal_df, normal_cdf, exp, ln


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
    dt: float = expiry_date/n_steps_time
    coef_1: float = dt*.5*(actual_vol**2 - implied_vol**2)*strike/implied_vol
    coef_2: float = (drift - interest + dividend)*dt

    t_list: [float] = [i*dt for i in range(n_steps_time)]
    sqrt_dt: float = dt**.5

    asset_prices: [float] = [asset_price0]
    for _ in range(n_steps_time-1):
        asset_prices.append(
            asset_prices[-1]
            * (1 + drift*dt + actual_vol*np.random.normal(0., sqrt_dt))
        )

    brownian_jump: [[float]] = [
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
        alpha: float = sigma * expiry_date**.5
        d1: float = (ln(asset_prices[i_t] / strike)
                     + (interest-dividend+sigma**2/2.)*expiry_date) / alpha
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
    for i_t in range(1, n_steps_time):
        tau = expiry_date - t_list[i_t]
        sqrt_tau = tau**.5
        exp_rtau = exp(-interest*tau)
        for sim in range(n_simulation):
            delta_a = delta(actual_vol, tau, i_t)[0]
            (delta_i, d1, d2) = delta(implied_vol, tau, i_t)
            dpnl[sim][i_t-1] = (
                coef_1*exp_rtau*normal_df(d2)/sqrt_tau
                + (coef_2 + actual_vol*brownian_jump[sim][i_t-1])
                * asset_prices[i_t] * (delta_i - delta_a)
            )

    interest_factor: float = exp(interest*dt)
    for sim in range(n_simulation):
        for i in range(n_steps_time-1):
            pnl[sim][i+1] = interest_factor*pnl[sim][i] + dpnl[sim][i]
        for i in range(1, n_steps_time):
            pnl[sim][i] *= exp(-interest*t_list[i])

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(t_list, asset_prices)
    for sim in range(n_simulation):
        ax2.plot(t_list, pnl[sim])
    plt.show()

from functions.BS_pricing import black_scholes_pricing
from functions.math_utility import get_delta, exp, generate_GBM
from matplotlib import pyplot as plt


plt.style.use('ggplot')


def hedging_strategie(
    underlying_prices: [float],
    time: [float],
    refresh_rate: int,
    interest: float,
    dividend: float,
    volatility: float,
    strike: float,
    maturity: float,
    option_type: str = "Call"
) -> None:
    option_prices: [float] = [
        black_scholes_pricing(
            price, strike, volatility,
            interest, maturity
        ) for price in underlying_prices
    ]
    taus: [float] = [time[-1] - t for t in time]
    portfolio_value: [float] = []
    deltas: [float] = [
        get_delta(
            underlying_prices[i], volatility, taus[i],
            strike, interest, dividend, option_type
        )[0] for i in range(0, len(time), refresh_rate)
    ]

    cash: [float] = [option_prices[0] - deltas[0]*underlying_prices[0]]
    pnl: [float] = [0.]
    last_action_index: int = 0
    for i in range(1, len(time)):
        cash.append(
            cash[-1]*exp(interest*(time[i]-time[i-1]))
            + dividend*deltas[last_action_index]*underlying_prices[i]
        )
        pnl.append(pnl[-1]*exp(interest*(time[i]-time[i-1])))
        if not i % refresh_rate:
            # Action on the portfolio
            last_action_index = i // refresh_rate
            pnl[-1] += cash[-1]
            cash[-1] = option_prices[i] - \
                deltas[last_action_index]*underlying_prices[i]
            pnl[-1] -= cash[-1]

    portfolio_value = [
        deltas[i//refresh_rate]*underlying_prices[i] + cash[i]
        for i in range(len(time))
    ]

    fig, axs = plt.subplots(4)
    axs[0].plot(time, underlying_prices)
    axs[1].plot(time, option_prices, label="Option price")
    axs[1].plot(time, portfolio_value, label="Portfolio value")
    axs[2].plot(
        time,
        [deltas[i//refresh_rate] for i in range(len(time))]
    )
    axs[3].plot(time, pnl)
    axs[0].set_title("Underlying price")
    axs[1].set_title("Strategy")
    axs[2].set_title("Hedge ratio")
    axs[3].set_title("P&L")
    for ax in axs.flat:
        ax.set(xlabel="Time in year", ylabel="Price")
        ax.label_outer()
    axs[1].legend()
    plt.show()


n_tics: int = 24*365
time: [float] = [i/n_tics for i in range(n_tics)]
hedging_strategie(
    underlying_prices=generate_GBM(100., 0.2, 0.2, time),
    time=time,
    refresh_rate=24,
    interest=0.21,
    dividend=0.,
    volatility=0.21,
    strike=100.,
    maturity=1.
)

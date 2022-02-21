from matplotlib import pyplot as plt
from functions.BS_pricing import black_scholes_pricing


plt.style.use('ggplot')


def show_option_curve(
    underlying_prices: [float],
    time: [float],
    strike: float,
    interest: float,
    volatility: [float] or [[float]],
    maturity: float,
    option_type: str = "Call"
) -> None:
    n_prices: int = len(underlying_prices)
    if type(volatility[0]) == float:
        for i in range(len(volatility)):
            volatility[i] = [volatility[i] for _ in range(n_prices)]
    option_prices: [[float]] = [[black_scholes_pricing(
        underlying_prices[i], strike, vol[i],
        interest, maturity - time[i], option_type
    ) for i in range(n_prices)] for vol in volatility]

    fig, axs = plt.subplots(2)
    axs[0].plot(time, underlying_prices)
    for op_price in option_prices:
        axs[1].plot(time, op_price)
    axs[0].set_title("Underlying price")
    axs[1].set_title("Option price")
    for ax in axs.flat:
        ax.set(xlabel="Time in year", ylabel="Price")
        ax.label_outer()
    plt.show()
